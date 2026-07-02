from common import pd, np, plt, SQL_DIR, RES_A_SUP, RESULTATS_DIR, get_db, run_chart, generate_distinct_colors

# Requete 10 : Camembert des moyennes d'issues par repo selon leur catégorie

def run(tab) :
	r10=open(SQL_DIR / "R10-nb_issues_1000lines-category.sql").read()
	df_plot = pd.read_sql_query(r10, tab)
# Pie chart
	plt.figure(figsize=(18, 10))
	colors= generate_distinct_colors(len(df_plot))
	plt.pie(
	    df_plot["avg_errors_per_repo"],
	    labels=df_plot["category"],
	    colors=colors,
	    autopct="%1.1f%%",
	    startangle=90
	)
	plt.title(
	    "Average Green issues per 1000 Lines by Repository Category",
	    fontweight="bold"
	)
	plt.tight_layout() 
	plt.savefig (RES_A_SUP / "R10-pie-nb_issues-categories.pdf", bbox_inches="tight")
# Bar chart
	df_plot = pd.read_sql_query(r10, tab)
	plt.figure(figsize=(18, 10))
	bars=plt.bar(
	    df_plot["category"],
	    df_plot["avg_errors_per_repo"],
	    color="green"
	)
	for bar, avg in zip(bars, df_plot["avg_errors_per_repo"]):
	    plt.text(
		bar.get_x()+bar.get_width()/3,
		bar.get_height()+0.03,
		f"{avg:.1f}",
		fontsize=12
	    )
	plt.xlabel("Categories", fontweight= "bold")
	plt.ylabel("Average Green Issues per 1000 Lines", fontweight= "bold")
	plt.title("Average Green Issues per 1000 Lines by Respository Category", fontweight="bold")
	plt.xticks(rotation=45, ha="right")
	plt.tight_layout()
	plt.savefig( RESULTATS_DIR / "R10-bar-nb_issues_1000lines-categories.pdf")

# Bar chart : issues/1000 lines
	
if __name__== "__main__" :
	run_chart(run)
