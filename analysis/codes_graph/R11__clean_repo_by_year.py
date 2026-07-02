from common import plt, pd, np, Line2D, RES_A_SUP, RESULTATS_DIR, SQL_DIR, get_db, run_chart


# Requete 11 : Diagramme bâton du nombre de repo avec 0 issue selon l'année

def run(tab) :
	r11=open(SQL_DIR / "R11-0issue_by_creation_year.sql").read()
	df11=pd.read_sql_query(r11, tab)
	df_plot = df11.copy()
	df_plot = df_plot.sort_values("year") 
	plt.figure(figsize=(14, 8))
	bars= plt.bar(
	   df_plot["year"].astype(str),
	   df_plot["nb_repos_zero_issue"],
	   color="green"
	)
	for bar, zero, total in zip(bars, df_plot["nb_repos_zero_issue"], df_plot["total_repos"]) :
		pct=(zero*100) /total if total > 0 else 0
		plt.text(
			bar.get_x() + bar.get_width()/2,
			bar.get_height(),
			f"{pct:.1f}%",
			ha="center",
			va="bottom",
			fontsize=9
		)
	plt.xlabel("Years", weight= "bold")
	plt.ylabel("Number of repositories with 0 issues", weight= "bold")
	plt.title("Zero-Issue Repositories Over Years", fontweight="bold")
	plt.xticks(rotation=45)
	plt.tight_layout()
	plt.savefig(RES_A_SUP / "R11-clean_repo_by_year.pdf")


# Requete 11-bis : 
	r11b=open(SQL_DIR / "R11b-pct-0issue_by_creation_year.sql").read()
	df11b=pd.read_sql_query(r11b, tab)
	df_plot = df11b.copy()
	df_plot = df_plot.sort_values("year")
	plt.figure(figsize=(18, 8))
	bars=plt.bar(
	    df_plot["year"].astype(str),
	    df_plot["pct_zero_issue"],
	    color="green"
	)
	for bar, total in zip(bars, df_plot["total_repos"]):
	    plt.text(
	        bar.get_x() + bar.get_width() / 2,
	        bar.get_height(),
	        str(total),
	        ha="center",
	        va="bottom",
	        fontsize=9
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
	plt.xlabel("Creation Year", weight = "bold")
	plt.ylabel("% of repositories with 0 issues", weight="bold")
	plt.title("Percentage of Repositories with No Issues by Creation Year", fontweight="bold")
	plt.xticks(rotation=45)
	plt.ylim(0, 40)
	plt.tight_layout()
	plt.savefig(RES_A_SUP / "R11b-%_clean_repo_by_year.pdf")

if __name__== "__main__":
	run_chart(run)
