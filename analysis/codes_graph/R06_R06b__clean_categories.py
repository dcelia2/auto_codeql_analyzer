from common import pd, plt, np, sqlite3, Line2D, RESULTATS_DIR, SQL_DIR, BASE_DIR, run_chart, get_db, generate_distinct_colors

# Requete 6 : Camembert des catégories classées par nombre de repo ayant 0 issue

def run(tab) :
	r=open(SQL_DIR / "R06-0issue_by_categories.sql").read()
	df=pd.read_sql_query(r, tab)
	others=df["repos_with_0_issue"].iloc[16:].sum()
	df_plot = pd.concat([
	    df.head(15),
	    pd.DataFrame([{
		"category":"Others",
		"repos_with_0_issue": others
	    }])
	])
	colors=generate_distinct_colors(16)
	plt.figure(figsize=(8, 8))
	plt.pie(
	    df_plot["repos_with_0_issue"],
	    labels=df_plot["category"],
	    colors=colors,
	    radius=0.85,
	    autopct="%1.1f%%",
	    startangle=25,
	    wedgeprops={
	        "edgecolor": "white",
	        "linewidth":1
	    },
	    textprops={"fontsize": 12}
	)
#	plt.title("Distribution of Repositories with 0 Green Issue by Category", fontweight="bold")
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R06-nb_clean_repo_by_categories.pdf")


# Requete 6-bis : Diagramme bâtons avec les pourcentages de repos qui ont 0 issue pour chaque categorie
	r=open(SQL_DIR / "R06b-pct_0issue_by_categories.sql").read()
	df=pd.read_sql_query(r, tab)
	df_plot = df.copy()
	plt.figure(figsize=(8, 8))
	bars= plt.bar(
	    df_plot["category"],
	    df_plot["percentage_zero_issue"],
	    color="green"
	)
	for bar, total in zip(bars, df["total_repos"]):
		plt.text(
			bar.get_x()+bar.get_width() / 2,
			bar.get_height(),
			f"{total}*",
			ha="center",
			va="bottom",
			fontsize=11
		)
	legend_item= Line2D(
	    [0], [0],
	    color="none",
	    label="* : Total number of repositories in the category"
	)
	plt.legend(
	    handles=[legend_item],
	    handlelength=0,
	    fontsize=12,
	    loc= "upper right"
	)
	plt.ylabel("% of repos with 0 green issue", fontweight= "bold", fontsize=14)
	plt.xlabel("Categories", fontweight= "bold", fontsize=14)
#	plt.title("Clean Repository Rate by Category", fontweight="bold", fontsize=14)
	plt.xticks(rotation=45, ha="right", fontsize=12)
	plt.yticks(fontsize=12)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R06b-clean_repo_rate_by_category.pdf")



if __name__== "__main__":
	run_chart(run)
