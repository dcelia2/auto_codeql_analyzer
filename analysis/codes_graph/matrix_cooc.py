from common import np, pd, plt, sns, SQL_DIR, RESULTATS_DIR, run_chart
from matplotlib.colors import LinearSegmentedColormap


def run(tab) :
	cooc = pd.read_sql_query("""
	        SELECT
	            er1.error_id AS error1,
	            er2.error_id AS error2,
	            COUNT(DISTINCT er1.repo_id) AS cooccurrence_count
	        FROM error_reports er1
	        JOIN error_reports er2
	            ON er1.repo_id = er2.repo_id
	           AND er1.error_id < er2.error_id
	        GROUP BY er1.error_id, er2.error_id
	        """, tab)
	errors = pd.read_sql_query("""
	SELECT
	    error_id,
	    error_name
	FROM error_catalog
	ORDER BY error_id
	""", tab)

	strength = cooc.groupby("error1")["cooccurrence_count"].sum()
	strength2 = cooc.groupby("error2")["cooccurrence_count"].sum()
	total_strength = strength.add(strength2, fill_value=0)
	ordered_errors = total_strength.sort_values(ascending=False).index.tolist()
	all_errors= set(errors["error_id"])
	isolated= list(all_errors - set(ordered_errors))

	ordered_issues = ordered_errors + isolated
	errors_ID = sorted(set(errors["error_id"]))
	id_to_name = dict(zip(errors["error_id"], errors["error_name"]))
	errors_names = [id_to_name[e] for e in ordered_issues]
	n = len(ordered_issues)
	index = {e: i for i, e in enumerate(ordered_issues)}

	# Matrice de cooccurrences
	matrix = np.zeros((n, n))
	for _, row in cooc.iterrows():
	    i = index[row["error1"]]
	    j = index[row["error2"]]
	    value = row["cooccurrence_count"]
	    matrix[i, j] = value
	    matrix[j, i] = value

#	 Palette de couleurs
#	colors = [
#	    "#ffffff",  # blanc
#	    "#fff7bc",  # jaune clair
#	    "#fec44f",  # jaune/orange
#	    "#f03b20",  # rouge
#	    "#000000"   # noir
#	]
	#cmap = LinearSegmentedColormap.from_list("cooc_map", color)

	# Figure
	colors= plt.cm.Blues(np.linspace(0.09,1,256))
	new_cmap = LinearSegmentedColormap.from_list(
	    "Blues_truncated",
	    colors
	)
	new_cmap.set_under("white")
	plt.figure(figsize=(9, 10))
	ax = sns.heatmap(
	    matrix,
	    cmap=new_cmap,
	    vmin=0.9,
	    linewidths=0.3,
	    linecolor="grey",
	    xticklabels=errors_names,
	    yticklabels=errors_names,
	    cbar_kws={
		"fraction":0.05,
		"pad": 0.02,
		"aspect":30
	    }
	)
	# Colorbar
	cbar = ax.collections[0].colorbar
	cbar.set_label("Number of co-occurrences", fontsize=8, fontweight="bold")
	ax.plot(
	    np.arange(n) + 0.5,
	    np.arange(n) + 0.5,
	    marker="x",
	    linestyle="None",
	    color="black"
	)

	plt.xticks(rotation=90, fontsize=9)
	plt.yticks(rotation=0, fontsize=9)
	plt.title(
	    "Co-occurrence Matrix of Green issues",
	    fontsize=12,
	    fontweight="bold"
	)
	plt.tight_layout()
	plt.savefig( RESULTATS_DIR / "matrix_cooccurrences.pdf", bbox_inches="tight")

# Matrice réduite
	cooc = cooc.sort_values(
	   "cooccurrence_count",
	   ascending=False
	).head(80)
	strength = cooc.groupby("error1")["cooccurrence_count"].sum()
	strength2 = cooc.groupby("error2")["cooccurrence_count"].sum()
	total_strength = strength.add(strength2, fill_value=0)
	ordered_issues = total_strength.sort_values(ascending=False).index.tolist()
	id_to_name = dict(zip(errors["error_id"], errors["error_name"]))
	errors_names = [id_to_name[e] for e in ordered_issues]
	n = len(ordered_issues)
	index = {e: i for i, e in enumerate(ordered_issues)}

	# Matrice de cooccurrences
	matrix = np.zeros((n, n))
	for _, row in cooc.iterrows():
	    i = index[row["error1"]]
	    j = index[row["error2"]]
	    value = row["cooccurrence_count"]
	    matrix[i, j] = value
	    matrix[j, i] = value

	# Figure
	plt.figure(figsize=(16, 14))
	labels = np.where(matrix > 0, matrix.astype(int), "")
	cbar = ax.collections[0].colorbar
	cbar.set_label("Number of co-occurrences", fontsize=12)
	ax = sns.heatmap(
	    matrix,
	    cmap='Blues',
	    linewidths=0.3,
	    linecolor="grey",
	    xticklabels=errors_names,
	    yticklabels=errors_names,
	    cbar=True,
	    annot=labels,
	    fmt=""
	)
	# Colorbar
	ax.plot(
	    np.arange(n) + 0.5,
	    np.arange(n) + 0.5,
	    marker="x",
	    linestyle="None",
	    color="black"
	)
	plt.xticks(rotation=90, fontsize=8)
	plt.yticks(rotation=0, fontsize=8)
	plt.title(
	    "Matrix of the main Co-occurrences between Green issues",
	    fontsize=16,
	    fontweight="bold"
	)
	plt.tight_layout()
	plt.savefig( RESULTATS_DIR / "reduced_matrix-main_cooccurrences.pdf")


if __name__== "__main__" :
	run_chart(run)

