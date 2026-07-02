from common import plt, pd, np, Path, SQL_DIR, RESULTATS_DIR, get_db, run_chart
from scipy.stats import linregress


# Requete 4 : Nombre d'erreur par repo en fonction du nombre de lignes du repo

def run(tab) :
	r4=open(SQL_DIR / "R04-nb_lines-nb_issues.sql").read()
	df4=pd.read_sql_query(r4, tab)
# Diagramme avec Classes équilibrées
	df4["lines_group"], bins = pd.qcut(
	    df4["nb_lignes"],
	    q=10,
	    retbins=True,
	    duplicates="drop"
	)
	labels = [
	    f"{round(bins[i], -1):.0f}-{round(bins[i+1], -1):.0f}"
	    for i in range(len(bins)-1)
	]
	df4["lines_group"] = pd.qcut(
	    df4["nb_lignes"],
	    q=len(labels),
	    labels=labels,
	    duplicates="drop"
	)
	df_grouped = df4.groupby("lines_group", observed= True)["total_errors"].mean()
	plt.figure(figsize=(18,8))
	bars=plt.bar(
	    df_grouped.index.astype(str),
	    df_grouped.values,
	    color="green"
	)
	for bar, avg in zip(bars, df_grouped) :
	    plt.text(
	        bar.get_x() + bar.get_width() /3,
	        bar.get_height()+0.2,
	        f"{avg:.1f}",
	        fontsize=12
	    )
	plt.xlabel("Lines of Code (Balanced Classes)", fontweight= "bold")
	plt.ylabel("Average number of Green issues per repo", fontweight= "bold")
	plt.title(
	    "Average number of Green issues per Repository by Repository Size",
	    fontweight="bold"
	)
	plt.xticks(rotation=45)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R04-binned-avg_nb_issues-nb_lines.pdf")

# Nuage de points + courbe de tendance (loglog)
# PAS SAUVEGARDE
	plt.figure(figsize=(18, 8))
	x = np.log(df4["nb_lignes"])
	y = np.log(df4["total_errors"])
	slope, intercept, r_value, p_value, std_err = linregress(x, y)
	plt.scatter(x, y, alpha=0.5)
	plt.plot(
	    x,
	    intercept + slope * x,
	    color="green"
	)
	plt.xlabel("Number of Lines (Log Scale)", fontweight= "bold")
	plt.ylabel("Number of Issues (Log Scale)", fontweight= "bold")
	plt.title("PAS SAUVEGARDE : Number of Issues by Repository Size (Log Scale)", fontweight="bold")
	plt.grid(True, which="both", linestyle="--", alpha=0.3)
	plt.xlim(3, 14)
	plt.ylim(-1, 10)
#	plt.savefig(RESULTATS_DIR / "R04-loglog-nb_issues-nb_lines-trend.pdf")

# Sans échelle log
# PAS SAUVEGARDE
	plt.figure(figsize=(18, 8))
	x = df4["nb_lignes"]/1000
	y = df4["total_errors"]
	slope, intercept, r_value, p_value, std_err = linregress(x, y)
	plt.scatter(x, y, alpha=0.5)
	plt.plot(
	    x,
	    intercept + slope * x,
	    color="green",
	    label=f"Tendance (R²={r_value**2:.2f})"
	)
	equation = f"y = {slope:.3f}x + {intercept:.2f}"
	plt.text(
	    0.98, 0.85,
	    equation,
	    transform=plt.gca().transAxes,
	    ha="right",
	    va="top",
	    fontsize=12,
	    fontweight="bold",
	    color="green"
	)
	plt.xlabel("Number of Lines (x 1000)", fontweight="bold")
	plt.ylabel("Number of Issues", fontweight= "bold")
	plt.title("PAS SAUVEGARDE : Number of Issues by Repository Size", fontweight="bold")
	plt.grid(True, linestyle="--", alpha=0.3)


# Sans echelle log et sans ouliers
# PAS SAUVEGARDE
	plt.figure(figsize=(18, 8))
	x = df4["nb_lignes"] / 1000
	y = df4["total_errors"]
	xlim=200
	ylim= 1500
	slope, intercept, r_value, p_value, std_err = linregress(x, y)
	y_pred = intercept + slope * x
	plt.scatter(x, y, alpha=0.5)
	plt.plot(
	    x,
	    intercept + slope * x,
	    color="green",
	    linewidth=2,
	    label=f"Tendance (R²={r_value**2:.2f})"
	)
	plt.xlim(0, xlim)
	plt.ylim(0, ylim)
	equation = f"y = {slope:.3f}x + {intercept:.2f}"
	plt.text(
	    0.98, 0.85,
	    equation,
	    transform=plt.gca().transAxes,
	    ha="right",
	    va="top",
	    fontsize=12,
	    fontweight="bold",
	    color="green"
	)
	plt.xlabel("Number of Lines (x 1000)", fontweight="bold")
	plt.ylabel("Number of Issues", fontweight="bold")
	plt.title("PAS SAUVEGARDE : Number of Issues by Repository Size (Outliers Removed)", fontweight="bold")
	plt.grid(True, linestyle="--", alpha=0.3)
	plt.tight_layout()
	

if __name__=="__main__" :
	run_chart(run)

