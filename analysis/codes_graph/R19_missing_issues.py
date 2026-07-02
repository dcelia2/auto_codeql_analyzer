from common import pd, plt, np, SQL_DIR, RESULTATS_DIR, get_db

def run(tab, issue_id, show) :
	r19=open( SQL_DIR / "R19-missing_issue_study.sql").read()
	df=pd.read_sql_query(r19, tab)
	plt.figure(figsize=(18,12))
	plt.scatter(
	  df["nb_lines"],
	  df["occurrence"],
	  alpha=0.5,
	  color = "green"
	)
	plt.xlabel("Number of Lines (Repo Size)", fontweight="bold")
	plt.ylabel("Occurrences of Selected Green Issues", fontweight="bold")
	plt.title(
	    "Repository Size vs 'Missing' Green Issue Occurrences",
	    fontweight="bold"
	)
	#Adjusting the axis limits
	plt.ylim(0,40)
	plt.xlim(0,200000)
	
	plt.tight_layout()
	plt.savefig(RESULTATS_DIR / "R19-issue_types" / "Missing-total.pdf")
	if show ==False:
		plt.close()


# 'Missing' individual issue
	query = """
	SELECT
	    r.id,
	    r.nb_lines,
	    SUM(er.occurrence_count)*1000/nb_lines AS total_occurrences
	FROM repos r
	JOIN error_reports er
	    ON r.id = er.repo_id
	JOIN error_catalog ec
	    ON er.error_id = ec.error_id
	WHERE ec.error_id = ?
	GROUP BY r.id, r.nb_lines;
	"""
	query_name="""
	SELECT error_name
	FROM error_catalog
	WHERE error_id= ?
	"""
	query_id="""
	SELECT error_id
	FROM error_catalog
	ORDER BY error_id
	"""

	if issue_id == 0 :
		id_list=pd.read_sql_query(query_id, tab)["error_id"].tolist()
		for issue in id_list :
		    run(tab, issue, False)
		return
	plt.figure(figsize=(12, 8))
	issue_name= pd.read_sql_query(
	   query_name,
	   tab,
	   params=(issue_id,)
	).iloc[0]["error_name"]

	df = pd.read_sql_query(query, tab, params=(issue_id,))
	plt.scatter(
	    df["nb_lines"],
	    df["total_occurrences"],
	    color="green",
	    alpha=0.6
	)
	plt.xlabel("Number of lines in repository", fontweight="bold")
	plt.ylabel("Occurrences of issue per 1000 lines", fontweight="bold")
	plt.title( issue_name, fontweight="bold")

	# Adjusting the axis limits
	plt.xlim(0,80000)
	plt.ylim(0,10)

	plt.tight_layout()
	name_save=issue_name.replace(" ", "_")
	plt.savefig(RESULTATS_DIR / "R19-issue_types"/ f"{name_save}.pdf")
	if show== False:
	    plt.close()


if __name__== "__main__":
	tab=get_db()
	issue_id=int(input("Enter the issue ID : "))
	run(tab,issue_id, True)
	plt.show()
	plt.close()
