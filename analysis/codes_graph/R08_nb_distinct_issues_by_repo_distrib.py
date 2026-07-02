from common import pd, plt, np, Line2D, SQL_DIR, RESULTATS_DIR, get_db, run_chart

# Requete 8 : Distribution de repos par nombre d'erreurs distinctes

def run(tab) :
	r8=open(SQL_DIR / "R08-distrib_repos-nb_distinct_issues.sql").read()
	df8=pd.read_sql_query(r8,tab)
	df_plot = df8.copy()

	order = [
	    "0 issue",
	    "1-2 issues",
	    "3-4 issues",
	    "5-6 issues",
	    "7-8 issues",
	    "9-10 issues",
	    "11-12 issues",
	    "13-14 issues",
	    "15-20 issues",
	    "20+ issues"
	]
	total_repos=df_plot["nb_repos"].sum()
	df_plot["categorie"] = pd.Categorical(df_plot["categorie"], categories=order, ordered=True)
	df_plot = df_plot.sort_values("categorie")
	plt.figure(figsize=(18, 12))
	bars=plt.bar(
	    df_plot["categorie"],
	    df_plot["nb_repos"],
	    color="green"
	)
	for bar, val in zip(bars, df_plot["nb_repos"]):
	   pct=(val*100)/ total_repos if total_repos > 0 else 0
	   plt.text(
		bar.get_x() + bar.get_width()/2,
		bar.get_height(),
            	f"{pct:.1f}%",
	        ha="center",
	        va="bottom",
	        fontsize=9
        )
	legend_item = Line2D(
	    [0], [0],
	    color="none",
	    label="%  :  Percentage of analysed repositories"
	)
	plt.legend(
	    handles=[legend_item],
	    loc="upper right",
	    handlelength=0
	)
	plt.xlabel("Distinct Green Issue Count", fontweight="bold")
	plt.ylabel("Number of repositories", fontweight="bold")
	plt.title("Distribution of Repositories by Number of Distinct Green Issues", fontweight="bold")
	plt.xticks(rotation=30, ha="right")
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R08-distrib-nb_distinct_issues_by_repo.pdf")
	

if __name__== "__main__":
	run_chart(run)
