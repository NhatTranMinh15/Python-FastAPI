from random import random, randrange
from bs4 import BeautifulSoup

import requests

male: set = {"Anthony"}
female: set = {"Mary"}
code = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "DC",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]
file1 = open("name1.txt", "a")
file2 = open("name2.txt", "a")

url = "https://www.ssa.gov/cgi-bin/namesbystate.cgi"
for c in code:
    for y in range(63):
        print(c, y)
        response = requests.post(url, data={"state": c, "year": 1960 + y})
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        names = [td.text for td in soup.find_all("td", align="center")]
        for i, name in enumerate(names):
            if i % 2 == 0:
                male.add(name)
            else:
                female.add(name)
print(male)
print(female)
print(len(male))
print(len(female))

for i in male:
    file1.write(i)
    file1.write("\n")
for i in female:
    file2.write(i)
    file2.write("\n")
for i in male:
    file1.write("\"")
    file1.write(i)
    file1.write("\",")
for i in female:
    file1.write("\"")
    file2.write(i)
    file1.write("\",")
