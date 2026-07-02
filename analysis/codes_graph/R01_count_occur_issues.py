from common import pd, np, plt, Path, SQL_DIR, RESULTATS_DIR, get_db, run_chart, generate_distinct_colors


# Requete 1 : Classement décroissant des erreurs par nb total d'apparition

def run(tab):
	query1 = SQL_DIR / "R01-top_erreurs.sql"
	query1 = query1.read_text()
	df1=pd.read_sql_query(query1, tab)

# Pie chart
	plt.figure(figsize=(16,8))
	others_sum = df1["total_occurrences"].iloc[14:].sum()
	df_plot = pd.concat([
	    df1.head(13),
	    pd.DataFrame([{
	        "error_name": "Others",
	        "total_occurrences": others_sum
	    }])
	])
	colors = generate_distinct_colors(len(df_plot))
	plt.pie(
	    df_plot["total_occurrences"],
	    labels=df_plot["error_name"],
	    colors=colors,
	    autopct='%1.1f%%',
	    wedgeprops={
		"edgecolor": "white",
		"linewidth":1
	    }
	)
	plt.title("Different types of green issues found", fontweight="bold")
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R01-pie-Nb_issues_by_types.pdf", bbox_inches="tight")

# Bar chart
	plt.figure(figsize=(20,15))
	bars=plt.barh(df1["error_name"], df1["total_occurrences"], height=0.6, color="green")
	for bar, total in zip(bars, df1["total_occurrences"]) :
	   plt.text(
		bar.get_width()+100,
		bar.get_y()+bar.get_height()/1.5,
		f"{total}",
		fontsize=10
	   )
	plt.xlabel("Total number of appearances", fontweight="bold")
	plt.ylabel("Types of green issues", fontweight="bold")
	plt.title("Most frequently found green issues in repos", fontweight="bold")
	plt.gca().invert_yaxis()
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R01-bar-Nb_issues_by_types.pdf")

# Top 10
	plt.figure(figsize=(20,15))
	df1=df1.head(10)
	bars=plt.barh(df1["error_name"], df1["total_occurrences"], height=0.6, color="green")
	for bar, total in zip(bars, df1["total_occurrences"]) :
	   plt.text(
		bar.get_width()+100,
		bar.get_y()+bar.get_height()/1.5,
		f"{total}",
		fontsize=12
	   )
	plt.xlabel("Total number of appearances", fontweight="bold")
	plt.ylabel("Types of green issues", fontweight="bold")
	plt.title("Most frequently found green issues in repos (Top 10)", fontweight="bold")
	plt.gca().invert_yaxis()
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R01-bar-Top10-Nb_issues_by_types.pdf")




if __name__=="__main__":
	run_chart(run)
