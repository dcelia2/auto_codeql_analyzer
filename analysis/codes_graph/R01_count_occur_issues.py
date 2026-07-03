from common import pd, np, plt, textwrap, SQL_DIR, RESULTATS_DIR, get_db, run_chart, generate_distinct_colors

# Requete 1 : Classement décroissant des erreurs par nb total d'apparition

def run(tab):
	query1 = SQL_DIR / "R01-top_erreurs.sql"
	query1 = query1.read_text()
	df1=pd.read_sql_query(query1, tab)

# Pie chart
	plt.figure(figsize=(9,9))
	others_sum = df1["total_occurrences"].iloc[10:].sum()
	df_plot = pd.concat([
	    df1.head(9),
	    pd.DataFrame([{
	        "error_name": "Others",
	        "total_occurrences": others_sum
	    }])
	])
	colors = generate_distinct_colors(len(df_plot))
	labels = [
	    textwrap.fill(label, width=25)
	    for label in df_plot["error_name"]
	]
	plt.pie(
	    df_plot["total_occurrences"],
	    labels=labels,
	    colors=colors,
	    radius = 0.7,
	    autopct='%1.1f%%',
	    textprops={"fontsize": 14},
	    wedgeprops={
		"edgecolor": "white",
		"linewidth":1.5
	    },
	    startangle=20
	)
#	plt.title("Different types of green issues found", fontweight="bold", fontsize=14)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R01-pie-Nb_issues_by_types.pdf", bbox_inches="tight")

# Bar chart
	plt.figure(figsize=(9,10))
	bars=plt.barh(df1["error_name"], df1["total_occurrences"], height=0.8, color="green")
	for bar, total in zip(bars, df1["total_occurrences"]) :
	   plt.text(
		bar.get_width()+80,
		bar.get_y()+bar.get_height()*7/8,
		f"{total}",
		fontsize=12
	   )
	   plt.xticks(fontsize=12) 
	   plt.yticks(fontsize=12)
	plt.xticks(plt.xticks()[0][::2])

	plt.xlabel("Total number of appearances", fontweight="bold", fontsize=14)
	plt.ylabel("Types of green issues", fontweight="bold", fontsize=14)
#	plt.title("Most frequently found green issues in repos", fontweight="bold", x=-0.7, ha="left")
	ax=plt.gca()
	ax.invert_yaxis()
	ax.margins(y=0)
	plt.xlim(0,df1["total_occurrences"].max() *1.2)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R01-bar-Nb_issues_by_types.pdf")

# Top 10
	plt.figure(figsize=(8,5))
	df1=df1.head(10)
	labels = [
	    textwrap.fill(name, width=30)
	    for name in df1["error_name"]
	]
	bars=plt.barh(labels, df1["total_occurrences"], height=0.6, color="green")
	for bar, total in zip(bars, df1["total_occurrences"]) :
	   plt.text(
		bar.get_width()+100,
		bar.get_y()+bar.get_height()/1.5,
		f"{total}",
		fontsize=12
	   )
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=13)
	plt.xlabel("Total number of appearances", fontweight="bold", fontsize=14)
	plt.ylabel("Types of green issues", fontweight="bold", fontsize=14)
#	plt.title("Most frequently found green issues in repos (Top 10)", fontweight="bold", fontsize=14)
	ax=plt.gca()
	ax.invert_yaxis()
	ax.margins(y=0)
	plt.xticks(plt.xticks()[0][::2])
	plt.xlim(0,df1["total_occurrences"].max() *1.3)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R01-bar-Top10-Nb_issues_by_types.pdf")




if __name__=="__main__":
	run_chart(run)
