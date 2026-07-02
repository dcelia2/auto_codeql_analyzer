from common import pd, plt, np, SQL_DIR, RES_A_SUP, RESULTATS_DIR, RES_A_SUP, get_db, run_chart

def run(tab) :
	r15=open(SQL_DIR / "R15-%0issue_repo-last_commit_date.sql").read()
	df=pd.read_sql_query(r15,tab)
	x = df["year"]
	y = df["percent_zero_issue"]
	totals = df["total_repos"]
	plt.figure(figsize=(10, 5))
	bars = plt.bar(x, y, color= "green")
	plt.xlabel("Last commit years", fontweight= "bold")
	plt.ylabel("% repos with 0 issue", fontweight= "bold")
	plt.title("Percentage of Repositories with No Issues by Repository Last Commit Year", fontweight= "bold")
	for bar, total in zip(bars, totals):
	    height = bar.get_height()
	    plt.text(
	        bar.get_x() + bar.get_width() / 2,
	        height,
	        str(total),
	        ha="center",
	        va="bottom",
	        fontsize=9
	)
	plt.ylim(0, 40) 
	plt.grid(axis="y", linestyle="--", alpha=0.3)
	plt.tight_layout()
	plt.savefig(RES_A_SUP / "R15-%_0issue-last_commit_year.pdf")


# Requete 15b : Durée de vie
	r15b=open(SQL_DIR / "R15b-%0issue_repo-lifetime.sql").read()
	df=pd.read_sql_query(r15b,tab)
	x = df["lifetime_bin"]
	y = df["percent_zero_issue"]
	totals = df["total_repos"]
	plt.figure(figsize=(10, 5))
	bars = plt.bar(x, y, color="green")
	plt.xlabel("Repos lifetime (Years)", fontweight="bold")
	plt.ylabel("% repos with 0 issue", fontweight="bold")
	plt.title("Percentage of Repositories with No Issues by Repository Lifetime", fontweight= "bold")
	for bar, total in zip(bars, totals):
	    plt.text(
	        bar.get_x() + bar.get_width() / 2,
	        bar.get_height(),
	        str(total),
	        ha="center",
	        va="bottom",
	        fontsize=9
	    )
	plt.ylim(0, 25)
	plt.grid(axis="y", linestyle="--", alpha=0.3)
	plt.savefig(RES_A_SUP / "R15b-%_0issue-lifetime_years.pdf")


if __name__== "__main__" :
	run_chart(run)
