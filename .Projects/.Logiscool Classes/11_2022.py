import csv
import pandas as pd
import matplotlib.pyplot as plt

# file = open("deniro.csv")
# data = csv.reader(file, skipinitialspace=True)
# for row in data:
#     print(', '.join(row))
# file.close()

# # Adatok formázása
# pd.set_option("display.max_rows", None)
# pd.set_option("display.width", 320)
# csvfile = pd.read_csv("deniro.csv", skipinitialspace=True, index_col="Year")
# print(csvfile)

# # Konkrét oszlopok kiíratása
# def columns(col):
#     pd.set_option("display.max_rows", None)
#     csvfile = pd.read_csv("deniro.csv", skipinitialspace=True, usecols=col)
#     print(csvfile)
#
# columns(["Score", "Title"])

# Oszlopok nevei
# csvfile = pd.read_csv("deniro.csv", skipinitialspace=True)
# list_of_cols = list(csvfile.columns)
# print(list_of_cols)

# # Legjobb film
# csvfile = pd.read_csv("deniro.csv", skipinitialspace=True, usecols=["Score", "Title"])
# max_score = max(csvfile["Score"])
# row = csvfile[csvfile["Score"] == max_score] # 1 sorú mátrix
# print("The best movie is: ", row.iloc[0][1], "and its score was", row.iloc[0][0])

# Legrosszabb film (év, pontszám)
# csvfile = pd.read_csv("deniro.csv", skipinitialspace=True, usecols=["Score", "Year"])
# min_score = min(csvfile["Score"])
# row = csvfile[csvfile["Score"] == min_score] # 1 sorú mátrix
# print("The worst movie's score is:", row.iloc[0][1], "and it was released in:", row.iloc[0][0])

# Filmek átlagpontszáma
# csvfile = pd.read_csv("deniro.csv", skipinitialspace=True, usecols=["Score"])
# avg = 0
# for i in csvfile["Score"]:
#     avg += i
# avg /= len(csvfile["Score"])
# print(round(avg, 3))

# Pontszámok alakulása
csvfile = pd.read_csv("deniro.csv", skipinitialspace=True, usecols=["Year", "Score"])
csvfile.plot(x="Year", y="Score", kind="scatter")
plt.title("Year-Score graph")
plt.show()
