from common import plt, pd, np, SQL_DIR, RESULTATS_DIR, run_chart

def run(tab) :
	r17=open( SQL_DIR / "R17-avg_nb_issue_distinct_by_category.sql").read()
	df17=pd.read_sql_query(r17,tab)
	df = df17.sort_values("avg_nb_error_types", ascending=True)
	plt.figure(figsize=(10, 6))
	plt.barh(
	    df["category"],
	    df["avg_nb_error_types"]
	)
	plt.xlabel(
	    "Average Number of Distinct Issue Types per Repository",
	    fontweight="bold"
	)
	plt.ylabel(
	    "Category",
	    fontweight="bold"
	)
	plt.title(
	    "Average Number of Distinct Issue Types per Repository by Category",
	    fontweight="bold")
	plt.tight_layout()


if __name__== "__main__" :
	run_chart(run)
