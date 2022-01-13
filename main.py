import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

state = []
cases = []
death = []
recovered = []

viz_base = "https://coronaclusters.in/"
source_code = requests.get(viz_base)     
plain = source_code.text    
soup = BeautifulSoup(plain,"html.parser")
det = soup.find("table", {"id" : "state-data-table"})
body = det.find("tbody")
row = body.find_all("tr")

s = 0
c = 0
for i in row:
    h = i.find_all("th")
    d = i.find_all("td")
    for j in h:
        c += 1
        if c == 30 or c == 31 or c == 39:
            continue
        state.append(j.text)
        for k in d:
            s += 1
            if s == 1:
                cases.append(k.text)
            elif s == 3:
                death.append(k.text)
            elif s == 5:
                recovered.append(k.text)
            elif s > 6:    
                s -= s

df = pd.DataFrame({"State" : state,
                   "Total cases" : cases,
                   "Total death" : death,
                   "Total recovered" : recovered})

# print(df)     # uncomment this to view the entire data

g_dict = {}
for key in state:
    for value in cases:
        g_dict[key] = int(value)
        cases.remove(value)
        break

g_dict = sorted(g_dict.items(), key=lambda x:x[1])
g_dict = dict(g_dict)

g_key = []
g_value = []
for key, value in g_dict.items():
    g_key.append(key)
    g_value.append(value)

plt.bar(g_key, g_value)
plt.xlabel("States")
plt.xticks(rotation = 90)
plt.ylabel("Total cases (in million)")
plt.ylim(0, 7000000)
plt.margins(x=0, y=0)
plt.title("Corona details bar")
plt.show()

