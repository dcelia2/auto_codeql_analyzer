from common import pd, np, plt, sqlite3, SQL_DIR, RES_A_SUP, RESULTATS_DIR, run_chart, get_db
import statsmodels.api as sm


def run(tab):
    r5 = open(SQL_DIR / "dens_erreurs_ligne-nb_etoiles.sql").read()
    df5 = pd.read_sql_query(r5, tab)
    plt.figure(figsize=(10, 6))
    q99 = df5["avg_error_density"].quantile(0.99)
    df_filtered = df5[df5["avg_error_density"] <= q99]
    df_filtered = df_filtered[df_filtered["stars"] > 0]
    plt.style.use("ggplot")
    x = df_filtered["avg_error_density"] * 1000
    y = df_filtered["stars"]
    plt.scatter(x, y, alpha=0.4)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_sorted = np.sort(x)
    plt.plot(
        x_sorted,
        p(x_sorted),
        linewidth=2,
        color="green"
    )

    plt.yscale("log")
    plt.ylim(min(y), max(y))

    plt.xlabel("Average Number of Issues per 1000 Lines", fontweight="bold")
    plt.ylabel("Stars", fontweight="bold")
    plt.title(
        "Repository Popularity vs Issue Density (per 1000 Lines)",
        fontweight="bold"
    )

    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        RES_A_SUP / "R5-stars-error_density_per_1000_lines.pdf",
        bbox_inches="tight"
    )




if __name__=="__main__" :
	run_chart(run)

