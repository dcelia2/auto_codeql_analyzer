from common import  BASE_DIR, SQL_DIR, RESULTATS_DIR, run_chart
import subprocess

def run(tab) :
	with open(RESULTATS_DIR / "R00-stats.txt","w") as f:
		subprocess.run(
		    ["sqlite3", BASE_DIR / "output.db"],
		    stdin=open(SQL_DIR / "R00-stats.sql"),
		    stdout=f
		)
		print((RESULTATS_DIR / "R00-stats.txt").read_text())
# English version
	with open(RESULTATS_DIR / "R00-english_stats.txt","w") as f:
		subprocess.run(
		    ["sqlite3", BASE_DIR / "output.db"],
		    stdin=open(SQL_DIR / "R00-english_stats.sql"),
		    stdout=f
		)
		print((RESULTATS_DIR / "R00-english_stats.txt").read_text())

if __name__== "__main__":
	run_chart(run)
