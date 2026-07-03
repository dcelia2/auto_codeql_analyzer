from common import plt, pd, np, SQL_DIR, RESULTATS_DIR, get_db, run_chart


def run(tab) :
	r12=open(SQL_DIR / "R12-nb_issues_by_1000lines-nb_lines.sql").read()
	df=pd.read_sql_query(r12, tab)
	x=df["nb_lignes"]
	y=df["issues_per_1000_lines"]
	log_x = np.log10(x)
	log_y = np.log10(y)
	coef = np.polyfit(log_x, log_y, 1)
	trend = np.poly1d(coef)
	x_sorted=np.sort(x)
	plt.figure(figsize=(7, 7))
	plt.xscale("log")
	plt.yscale("log")
	plt.scatter(x, y, alpha=0.5, color="green")
	plt.plot(
	    x_sorted,
	    10**trend(np.log10(x_sorted)),
	    color="red",
	    linewidth=1
	)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlabel("Number of Lines in Repository (log scale)", fontweight= "bold", fontsize=14)
	plt.ylabel("Green Issues per 1000 Lines (log scale)", fontweight= "bold", fontsize=14)
#	plt.title("Green Issue Density vs Repository Size", fontweight= "bold")
	plt.grid(True, linestyle="--", alpha=0.4)
	plt.savefig(RESULTATS_DIR / "R12-nb_issues_by_1000lines-nb_lines.pdf")

# Test sans log 
	plt.figure(figsize=(16,14))
	plt.scatter(x,y,alpha=0.5, color="green")
	plt.xlim(0,300000)
	plt.ylim(0,30)
	plt.xlabel("Number of lines in Repositories")
	plt.ylabel("Green issues per 1000 lines")
#	plt.title("Green issue Density vs Repository Size", fontweight="bold")


if __name__== "__main__" :
	run_chart(run)
