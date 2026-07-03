from common import pd, plt, np, Path, textwrap, RESULTATS_DIR, SQL_DIR, get_db, run_chart, generate_distinct_colors
from matplotlib import cm

# Query 7: Sorting issues by frequency into distinct repositories

def run(tab) :
# Pie
	r7=open(SQL_DIR/ "R07-top_issues-distinct_repos.sql").read()
	df7=pd.read_sql_query(r7, tab)
	df7["error_name"].isna().sum()
	df_plot = df7.sort_values("nb_repos", ascending=False)
	top_n = 12
	colors = generate_distinct_colors(top_n+1)
	top = df_plot.head(top_n).copy()
	others_sum = df_plot.iloc[top_n:]["nb_repos"].sum()
	pie_df = pd.concat([
	    top,
	    pd.DataFrame({
	        "error_name": ["Others"],
	        "nb_repos": [others_sum]
	    })
	])
	plt.figure(figsize=(9,9))
	labels = [
	    textwrap.fill(label, width=30)
	    for label in pie_df["error_name"]
	]
	plt.pie(
	    pie_df["nb_repos"],
	    labels=labels,
	    colors=colors,
	    autopct="%1.1f%%",
	    startangle=40,
	    radius=0.7,
	    wedgeprops={
	        "edgecolor": "white",
	        "linewidth":1.5
	    },
	    textprops={
		"fontsize": 12
	    }
	)
#	plt.title("Green Issue Types by Distinct Repositories", fontweight="bold", fontsize=14)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R07-pie-nb_issues_by_distinct_repos.pdf")

# bar
	plt.figure(figsize=(8,15))
	df7=df7.sort_values("nb_repos", ascending=True)
	bars=plt.barh(df7["error_name"], df7["nb_repos"], color="green", height=0.6)
	for bar, nb_repos in zip(bars, df7["nb_repos"]) :
	    plt.text(
	       bar.get_width()+8,
	       bar.get_y()+bar.get_height()/8,
	       f"{nb_repos}",
	       fontsize=12
	    )
	ax=plt.gca()
	ax.margins(y=0)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlim(0,df7["nb_repos"].max() *1.2)
	plt.xlabel("Number of Repositories", fontweight="bold", fontsize=14)
	plt.ylabel("Green Issue types", fontweight="bold", fontsize=14)
#	plt.title("Most Common Distinct Green Issues by Repository Coverage", fontweight="bold", fontsize=16)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R07-bar-nb_issues_by_distinct_repos.pdf")


# bar (TOP 10)
	df7=df7.sort_values("nb_repos", ascending=False)
	df7=df7.head(10)
	df7=df7.sort_values("nb_repos", ascending=True)
	plt.figure(figsize=(6,6))
	labels = [
	    textwrap.fill(label, width=25)
	    for label in df7["error_name"]
	]
	bars=plt.barh(labels, df7["nb_repos"], color="green", height=0.6)
	for bar, nb_repos in zip(bars, df7["nb_repos"]) :
	    plt.text(
	        bar.get_width()+5,
	        bar.get_y() + bar.get_height()/6,
	        f"{nb_repos}",
	        fontsize=12
	    )
	plt.xlim(0,df7["nb_repos"].max() *1.3)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlabel("Number of Repositories",  fontweight="bold", fontsize=14)
	plt.ylabel("Green Issue types", fontweight="bold", fontsize=14)
#	plt.title("The 10 Most Common Green Issues by Repository Coverage", fontweight="bold")
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R07-bar-Top10-nb_issues_by_distinct_repos.pdf")


if __name__ == "__main__" :
	run_chart(run)
