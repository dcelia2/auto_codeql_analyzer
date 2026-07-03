from common import plt, pd, np, Path, SQL_DIR, RESULTATS_DIR, get_db, run_chart

# Requete 3 : Calcul de la moyenne du nombre de problèmes par repos pour chaque nb d'étoile

def run(tab) :
	r3=open(SQL_DIR / "R03-nb_issues-nb_stars.sql").read()
	df3=pd.read_sql_query(r3,tab)

	df3["etoiles_group"], bins = pd.qcut(
	    df3["nb_etoiles"],
	    q=10,
	    retbins=True,
	    duplicates="drop"
	)
	labels = [
	    f"{round(bins[i], -1):.0f}-{round(bins[i+1], -1):.0f}"
	    for i in range(len(bins) - 1)
	]
	
	df_grouped = df3.groupby("etoiles_group", observed=True)["moy_prob_par_repo"].mean()

	# Tracé du diagramme (en barres) avec classes
	plt.figure(figsize=(6, 6))
	bars=plt.bar(
	    labels,
	    df_grouped.values,
	    color="green"
	)
	for bar, avg in zip(bars, df_grouped) :
	    plt.text(
	       bar.get_x()+bar.get_width()/8,
	       bar.get_height()+0.1,
	       f"{avg:.1f}",
	       fontsize=12
	   )
	plt.xlabel("Star classes (balanced classes)", fontweight= "bold", fontsize=14)
	plt.ylabel("Average Green Issues per 1000 lines", fontweight= "bold", fontsize=14)
#	plt.title("Average Green Issues per 1000 Lines by Repository Star Range", fontweight="bold", fontsize=14)
	plt.xticks(rotation=45, fontsize=12)
	plt.yticks(fontsize=12)
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R03-nb_issues-nb_stars.pdf")
	
if __name__ == "__main__":
	run_chart(run)
