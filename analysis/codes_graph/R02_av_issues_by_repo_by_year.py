from common import pd, np, plt, Path, Line2D, SQL_DIR, RES_A_SUP, RESULTATS_DIR, RES_A_SUP, get_db, run_chart
from scipy.stats import linregress
import matplotlib.dates as mdates


# Requete 2 : Calcul du nombre moyen d'erreurs par repos pour chaque année 

def run(tab) :
	r2=open(SQL_DIR / "R02-nb_issues_1000lines-creation_year.sql").read()
	df2=pd.read_sql_query(r2,tab)
# Bar chart + Tendency
	plt.figure(figsize=(16,10))
	bars=plt.bar(df2["year"], df2["occ_par_repo"], color="green")
	plt.xlabel("Year of creation",fontweight= "bold")
	plt.ylabel("Issues per 1000 lines (avg)", fontweight= "bold")
	x = df2["year"].astype(int)
	y = df2["occ_par_repo"]
	for bar, n in zip(bars, df2["nb_repos"]):
		plt.text(
			bar.get_x() + bar.get_width()/2,
			bar.get_height(),
			str(n),
			ha="center",
			va="bottom",
			fontsize=9
		)
	slope, intercept, r_value, p_value, std_err = linregress(x, y)
	x_trend = np.sort(x)
	y_trend = intercept + slope * x_trend
	plt.plot(
	    x_trend,
	    y_trend,
	    color="red",
	    linewidth=1
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
	plt.title("Average number of issues per 1000 lines according to the repo year of creation", fontweight= "bold")
	plt.tight_layout()
	plt.savefig(RES_A_SUP / "R02-bar-nb_issues-year-tendency.pdf", bbox_inches="tight")



# Nuage de points
	r2 = open(SQL_DIR / "R02-cloud-nb_issues_1000lines-creation_date.sql").read()
	df2 = pd.read_sql_query(r2, tab)
	df2["date"] = pd.to_datetime(df2["date"], errors="coerce")
	df2 = df2.dropna(subset=["date", "avg_occurrences_per_repo"])
	x = df2["date"]
	y = df2["avg_occurrences_per_repo"].astype(float)
	plt.figure()
	plt.scatter(x, y)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
	plt.gcf().autofmt_xdate()
	x_num = mdates.date2num(x)
	slope, intercept, r_value, p_value, std_err = linregress(x_num, y)
	x_trend = np.linspace(x_num.min(), x_num.max(), 100)
	y_trend = slope * x_trend + intercept
	plt.plot(
	    mdates.num2date(x_trend),
	    y_trend,
	    color="green",
	    linewidth=2,
	    label=f"Tendency (R²={r_value**2:.2f})"
	)
	equation = f"y = {slope:.3f}x + {intercept:.2f}"
	plt.text(
	    0.98, 0.85,
	    equation,
	    transform=plt.gca().transAxes,
	    ha="right",
	    va="top",
	    color="green",
	    fontweight="bold"
	)
	plt.ylim(0, 20)
	plt.xlabel("Creation date", fontweight="bold")
	plt.ylabel("Average Number of Issues per 1000 lines", fontweight="bold")
	plt.title("Average Number of Problems per Repository over time", fontweight="bold")
	plt.legend()
	plt.tight_layout()
	plt.savefig( RES_A_SUP / "R02-cloud-nb_issues-creation_date-trend.pdf")


if __name__=="__main__" :
	run_chart(run)
