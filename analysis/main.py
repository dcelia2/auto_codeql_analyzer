import matplotlib.pyplot as plt
import sqlite3

import codes_graph.R00_stats as q0
import codes_graph.R01_count_occur_issues as q1
import codes_graph.R02_av_issues_by_repo_by_year as q2
import codes_graph.R03_nb_issues_nb_stars as q3
import codes_graph.R04_nb_issues_nb_lines as q4
import codes_graph.R06_R06b__clean_categories as q6_q6b
import codes_graph.R07_top_distinct_issues_by_repo as q7
import codes_graph.R08_nb_distinct_issues_by_repo_distrib as q8
import codes_graph.R09_avg_issues_occurence_by_type as q9
import codes_graph.R10_nb_issues_1000lines_by_category as q10
import codes_graph.R11__clean_repo_by_year as q11_q11b
import codes_graph.R12_nb_issues_1000lines_by_nb_lines as q12
import codes_graph.R13_nb_issues_by_1000lines_last_commit_date as q13
import codes_graph.R14_R14b_nb_issues_lifetime as q14_q14b
import codes_graph.R15_R15b_pct_0issue_last_commit as q15_q15b
import codes_graph.R16_nb_issue_total_and_distinct as q16
import codes_graph.R17_avg_nb_issues_distinct_by_category as q17

import codes_graph.R19_missing_issues as q19
import codes_graph.matrix_cooc as mat_cooc


Requetes=[
	q0, q1, q2, q3, q4, q6_q6b, q7, q8, q9, q10, q11_q11b, q12, q13, q14_q14b,
	q15_q15b, q16, q17,
	mat_cooc
]


tab=sqlite3.connect("../output.db")

if __name__ == "__main__":
    i=0
    for q in Requetes:
        if i==5:
           i=i+1
        print("Generating charts for query no. ", i, " in progress")
        q.run(tab)
        plt.close()
        i=i+1
    print("Generating charts for query no. ", i, " in progress")
    # R19
    q19.run(tab, 0, False)
    print("Generation complete. Results stored in : auto_codeql_analyzer/analysis/results")
