from common import plt, pd, np, Path, RESULTATS_DIR, SQL_DIR, get_db, run_chart

# Requete 9 : pour chaque type d’erreur → la moyenne d’occurrences dans les repos où elle apparaît
def run(tab) :
	r9=open(SQL_DIR / "R09-avg_issue_types_appear_by_repo.sql").read()
	df9=pd.read_sql_query(r9, tab)

	df_plot=df9.sort_values("avg_occurrences_per_repo", ascending=True)
	plt.figure(figsize=(20,18))
	bars=plt.barh(
	    df_plot["error_name"],
	    df_plot["avg_occurrences_per_repo"],
	    color="green"
	)
	for bar, avg in zip(bars, df_plot["avg_occurrences_per_repo"]):
	   plt.text(
	       bar.get_width()+0.1,
	       bar.get_y() + bar.get_height()/3,
	       f"{avg:.1f}",
	       fontsize=12
	   )
	plt.xlabel("Average occurrences per repo", fontweight="bold")
	plt.ylabel("Green Issues types", fontweight="bold")
	plt.title("Average Green Issue Occurrence per Repository (by Green Issue Type)", fontweight="bold")
	plt.tight_layout()
	plt.savefig( RESULTATS_DIR / "R09-avg_issue_occurrence_by_type.pdf")

# TOP 10
	df_plot = df9.head(10).copy()
	df_plot = df_plot.sort_values("avg_occurrences_per_repo", ascending=True)
	plt.figure(figsize=(20, 18))
	bars=plt.barh(
	   df_plot["error_name"],
	   df_plot["avg_occurrences_per_repo"],
	   color="green"
	)
	for bar, avg in zip(bars, df_plot["avg_occurrences_per_repo"]):
	    plt.text(
	       bar.get_width()+0.2,
	       bar.get_y()+bar.get_height()/2,
	       f"{avg:.1f}",
	       fontsize=12
	    )
	plt.xlabel("Average occurrences per repo", fontweight="bold")
	plt.ylabel("Green Issue types", fontweight="bold")
	plt.title("Top 10-Average Green Issue Occurrence per Repository (by Green Issue Type)", fontweight="bold")
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R09-Top10-avg_issue_occurrence_by_type.pdf")

if __name__ ==  "__main__" :
	run_chart(run)
