from common import pd, plt, np, SQL_DIR, RESULTATS_DIR, get_db, run_chart


def run(tab) :
	r16=open(SQL_DIR / "R16-nb_issue_total-nb_issue_distinct.sql").read()
	df16=pd.read_sql_query(r16,tab)
	df=df16.head(10)
	df=df.sort_values("total_occurrences", ascending=True)
	df["distinct_ratio"] = (
 	   df["distinct_repos"] / df["total_occurrences"] * 100
	)
	plt.figure(figsize=(8, 6))
	plt.barh(
	    df["error_name"],
	    df["total_occurrences"],
	    label= "Total occurrences",
	    color="white",
	    edgecolor="black",
	    hatch="/"
	)
	plt.barh(
	    df["error_name"],
	    df["distinct_repos"],
	    label="Distinct repositories",
	    color="green"
	)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlabel("Number of Green Issues", fontweight="bold", fontsize=14)
	plt.ylabel("Green Issue Types", fontweight="bold", fontsize=14)
#	plt.title("Top 10 Green Issue types by Occurrences and Repository Coverage", fontweight="bold")
	for i, (name, ratio) in enumerate(zip(df["error_name"], df["distinct_ratio"])):
	    plt.text(
	        2200, i,  
	        f"{ratio:.1f}%",
	        va="center",
	        ha="right",
	        fontweight="bold",
		fontsize=12
	    )
	plt.legend()
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R16-nb_issues_total_and_distinct.pdf")



if __name__== "__main__":
	run_chart(run)
