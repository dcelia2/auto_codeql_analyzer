from common import plt, pd, np, SQL_DIR, RES_A_SUP, RESULTATS_DIR, run_chart


def run(tab):
	r18=open(SQL_DIR / "R18-0issue-1more_issue-last_update.sql").read()
	df=pd.read_sql_query(r18, tab)
	plt.figure(figsize=(12, 8))
# Requete 18 : Last Commit
	bars=plt.bar(
	    df["last_commit"],
	    df["total_occurrences"],
	    color="white",
	    edgecolor="black",
	    hatch="//",
	    label="Total repositories"
	)
	for bar, total in zip(bars, df["total_occurrences"]) :
	    plt.text(
		bar.get_x() + bar.get_width()/3,
		bar.get_height()+30,
		f"{total}",
		fontsize=12
	    )
	bars = plt.bar(
	    df["last_commit"],
	    df["repos_0_issue"],
	    color="green",
	    label="Repositories with 0 issue"
	)
	for bar, without_issue, total in zip(
	    bars,
	    df["repos_0_issue"],
	    df["total_occurrences"]
	):
	    pct = 100 * without_issue / total if total else 0
	    plt.text(
	        bar.get_x() + bar.get_width()/3,
	        bar.get_height()+4,
	        f"{pct:.1f}%",
		fontsize=9,
		fontweight="bold"
	    )
	plt.xlabel("Last Commit Year", fontweight="bold")
	plt.ylabel("Number of Repositories", fontweight="bold")
	plt.title(
	    "Repositories with Issues by Last Commit Year",
	    fontweight="bold"
	)
	plt.legend()
	plt.tight_layout()
	plt.savefig(RES_A_SUP / "R18-0issue-1more_issues-last_update.pdf")


# Requete 18 bis : Creation date
	r18b=open(SQL_DIR / "R18b-0issue-1more_issue-creation_date.sql").read()
	df=pd.read_sql_query(r18b, tab)
	plt.figure(figsize=(18,8))
	bars=plt.bar(
	    df["creation_year"],
	    df["total_occurrences"],
	    color="white",
	    edgecolor="black",
	    hatch="//",
	    label="Total repositories"
	)
	for bar2, without_issue, total in zip( bars, df["creation_year"], df["total_occurrences"]) :
	    plt.text(
		bar2.get_x() + bar2.get_width()/2.5,
		bar2.get_height()+4,
		f"{total}",
		fontsize=12
	    )

	bars = plt.bar(
	    df["creation_year"],
	    df["repos_0_issue"],
	    color="green",
	    label="Repositories with 0 issue"
	)
	for bar, without_issue, total in zip(
	    bars,
	    df["repos_0_issue"],
	    df["total_occurrences"]
	):
	    pct = 100 * without_issue / total if total else 0
	    plt.text(
	        bar.get_x() + bar.get_width()/2,
	        bar.get_height() +2.5,
	        f"{pct:.1f}%",
	        ha="center",
	        va="bottom",
	        fontsize=9,
		fontweight="bold"
	    )
	plt.xlabel("Creation Year", fontweight="bold")
	plt.ylabel("Number of Repositories", fontweight="bold")
	plt.title(
	    "Repositories with Issues by Creation Year",
	    fontweight="bold"
	)
	plt.legend()
	plt.tight_layout()
	plt.savefig(RES_A_SUP / "R18b-0issue-1more_issues-creation_year.pdf")


if __name__== "__main__":
	run_chart(run)
