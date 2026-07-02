from common import pd, plt, np, mpatches, SQL_DIR, RESULTATS_DIR, RES_A_SUP, get_db, run_chart, Line2D

def run(tab) :
# Bar chart
	r13 = open(SQL_DIR / "R13-nb_issues_1000lines-last_commit_year.sql").read()
	df2 = pd.read_sql_query(r13, tab)
	df2["year"] = pd.to_numeric(df2["year"], errors="coerce")
	df2["avg_occurrences_per_repo"] = pd.to_numeric(df2["avg_occurrences_per_repo"], errors="coerce")
	df2 = df2.dropna()
	df2 = df2.sort_values("year")
	plt.figure(figsize=(10, 6))
	bars = plt.bar(
	    df2["year"].astype(int),
	    df2["avg_occurrences_per_repo"],
	    color="green"
	)
	for i, bar in enumerate(bars):
	    year = df2["year"].iloc[i]
	    nb = df2["nb_repos"].iloc[i]
	    plt.text(
	        bar.get_x() + bar.get_width()/2,
	        bar.get_height(),
	        f"{nb}",
	        ha="center",
	        va="bottom"
	    )
	legend_text = Line2D(
	    [0], [0],
	    marker=r"${0~0~0}$",
	    color="black",
	    linestyle="None",
	    markersize=20,
	    label="Number of repositories"
	)
	plt.legend(handles=[legend_text])
	plt.xlabel("Years of last commit", fontweight= "bold")
	plt.ylabel("Avg issues per 1000 lines per repo", fontweight= "bold")
	plt.title("Issues density per repository by last commit year ", fontweight= "bold")
	plt.tight_layout()
	plt.savefig(RES_A_SUP / "R13-avg-nb_issues_by_1000lines-last_commit_year.pdf")


if __name__== "__main__" :
	run_chart(run)
