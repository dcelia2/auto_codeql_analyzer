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
	plt.figure(figsize=(8,8))
	bars=plt.bar(
	    df_grouped.index.astype(str),
	    df_grouped.values,
	    color="green"
	)
	for bar, avg in zip(bars, df_grouped) :
	    plt.text(
	        bar.get_x() + bar.get_width() /8,
	        bar.get_height()+0.2,
	        f"{avg:.1f}",
	        fontsize=12
	    )
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlabel("Lines of Code (Balanced Classes)", fontweight= "bold", fontsize=14)
	plt.ylabel("Average number of Green issues per repo", fontweight= "bold", fontsize=14)
#	plt.title("Average number of Green issues per Repository by Repository Size", fontweight="bold")
	plt.xticks(rotation=45)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R04-binned-avg_nb_issues-nb_lines.pdf")
 

if __name__=="__main__" :
	run_chart(run)

