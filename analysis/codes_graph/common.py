import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import runpy # pour utiliser run depuis le fichier main.py
import colorsys # permet de définir les couleurs des camemberts
import seaborn as sns # pour utiliser les echelles de couleur
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D


BASE_DIR = Path.home() / "auto_codeql_analyzer"
SQL_DIR= BASE_DIR / "analysis/sql_queries"
RESULTATS_DIR= BASE_DIR / "analysis/results"
RES_A_SUP = BASE_DIR / "analysis/res_sup"


def get_db():
	return sqlite3.connect(BASE_DIR / "output.db")


def run_chart(run) :
	tab=get_db()
	run(tab)
	plt.show()
	plt.close()


def generate_distinct_colors(n):
        colors = []
        start_hue= 0.1
        end_hue= 0.8
        for i in range(n):
                hue = start_hue + i * (end_hue -start_hue) / max(n - 1, 1)
                saturation = 0.65
                value = 0.90
                colors.append(colorsys.hsv_to_rgb(hue%1, saturation, value))
        return colors

