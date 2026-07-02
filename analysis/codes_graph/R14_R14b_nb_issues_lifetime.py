from common import np, plt, pd, SQL_DIR, RESULTATS_DIR, RES_A_SUP, run_chart, get_db

def run(tab) :
# Nuage de points + Tendance
	r14=open(SQL_DIR / "R14-avg_issues_by_repo_lifetime.sql").read()
	df=pd.read_sql_query(r14, tab)
	x = df["lifetime_years"]
	y = df["issues_per_1000_lines"]
	coef = np.polyfit(x, y, 1)
	trend = np.poly1d(coef)
	x_sorted = np.sort(x)
	plt.figure(figsize=(10, 6))
	plt.scatter(x, y, alpha=0.6)
	plt.plot(
	    x_sorted,
	    trend(x_sorted),
	    color="red",
	    linewidth=1.5,
	    label="Trend Line"
	)
	plt.xlabel("Repository Lifetime (Years)", fontweight= "bold")
	plt.ylabel("Issues /1000 lines", fontweight= "bold")
	plt.title("Repository Lifetime vs Issues per 1000 lines", fontweight= "bold")
	plt.ylim(0,60)
	plt.grid(True, linestyle="--", alpha=0.4)
	plt.legend()
	plt.savefig(RES_A_SUP / "R14-nb_issues_1000lines-lifetime.pdf")


    # Nuage de points + Tendance
#	r14 = open(SQL_DIR / "R14-color_issues_by_types-repo_lifetime.sql").read()
#	df = pd.read_sql_query(r14, tab)
#	top_errors = df["dominant_error"].value_counts().head(10).index
#	df.loc[
#	    ~df["dominant_error"].isin(top_errors),
#	    "dominant_error"
#	] = "Other"
#	x = df["lifetime_years"]
#	y = df["issues_per_1000_lines"]
#	coef = np.polyfit(x, y, 1)
#	trend = np.poly1d(coef)
#	x_sorted = np.sort(x)
#	plt.figure(figsize=(10, 6))
#	for error_name in sorted(df["dominant_error"].unique()):
#		subset = df[df["dominant_error"] == error_name]
#		plt.scatter(
#		    subset["lifetime_years"],
#		    subset["issues_per_1000_lines"],
#		    alpha=0.6,
#		    s=20,
#		    label=error_name
#		)
#	plt.plot(
#	     x_sorted,
#	     trend(x_sorted),
#	     color="red",
#	     linewidth=1.5,
#	     label="Trend Line"
#	)
#	plt.xlabel(
#	    "Repository Lifetime (Years)",
#	    fontweight="bold"
#	)
#	plt.ylabel(
#	     "Issues / 1000 Lines",
#	     fontweight="bold"
#	)
#	plt.title(
#	    "Repository Lifetime vs Issues per 1000 Lines",
#	    fontweight="bold"
#	)
#	plt.ylim(0, 60)
#	plt.grid(True, linestyle="--", alpha=0.4)
#	plt.legend(
#	    title="Dominant Issue",
#	    bbox_to_anchor=(1.05, 1),
#	    loc="upper left",
#	    fontsize=8
#	)
#	plt.tight_layout()
	#plt.savefig(
        #RESULTATS_DIR / "R14-nb_issues_1000lines-lifetime.pdf"
	#    )

# TEST
	df = pd.read_sql_query(
		open(SQL_DIR / "R14-color_issues_by_types-repo_lifetime.sql").read(),
		tab
	)
	top8 = (
	    df["dominant_error"]
	    .value_counts()
	    .head(8)
	    .index
	)
	df["dominant_error"] = df["dominant_error"].where(
	    df["dominant_error"].isin(top8),
	    "Other"
	)
	plt.figure(figsize=(18, 8))
	for err in df["dominant_error"].unique():
	    subset = df[df["dominant_error"] == err]
	    if err == "Other":
	        plt.scatter(
	            subset["lifetime_years"],
	            subset["issues_per_1000_lines"],
	            alpha=0.2,   # 👈 ici
	            s=20,
	            label=err
	        )
	    else:
	        plt.scatter(
	            subset["lifetime_years"],
	            subset["issues_per_1000_lines"],
	            alpha=0.7,
	            s=25,
	            label=err
	        )
	plt.xlabel("Repository Lifetime (Years)")
	plt.ylabel("Issues per 1000 Lines")
	plt.ylim(0,60)
	plt.title("Repo Lifetime vs Issue Density (dominant error ≥5%)")
	plt.grid(True, linestyle="--", alpha=0.4)
	plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
	plt.tight_layout()



# Requete 14-bis : diagramme baton par année de durée de vie
	r14b=open(SQL_DIR / "R14b-avg-issues_1000lines-year_lifetime.sql").read()
	df=pd.read_sql_query(r14b, tab)
	plt.figure(figsize=(10, 6))
	bars = plt.bar(
	    df["lifetime_years_bin"].astype(str),
	    df["avg_issues_per_1000_lines"],
	    color="green",
	    alpha=0.7
	)
	for bar, count in zip(bars, df["repo_count"]):
	    plt.text(
	        bar.get_x() + bar.get_width()/2,
	        bar.get_height(),
	        str(count),
	        ha="center",
	        va="bottom",
	        fontsize=9
	    )
	plt.xlabel("Repository Lifetime (Years-binned)", fontweight= "bold")
	plt.ylabel("Average Issues per 1000 Lines", fontweight= "bold")
	plt.title("Issue Density by Repository Lifetime", fontweight= "bold")
	plt.grid(axis="y", linestyle="--", alpha=0.4)
	plt.savefig(RES_A_SUP/"R14b-nb_issues_1000lines-year_lifetime-binned.pdf")


if __name__== "__main__":
	run_chart(run)
