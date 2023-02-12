from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
import matplotlib.pyplot as plt

import requests
page = requests.get("https://www.imdb.com/list/ls055592025/")
page_soup = soup(page.content, 'html.parser')
film_list = page_soup.find_all(class_= "lister-item mode-detail")

ranks = []
titles = []
ratings = []
#gross = []
years = []
runtimes = []

for film in film_list:
    ranks.append(int(film.find(class_= "lister-item-index unbold text-primary").get_text()[0:-1]))
    titles.append(film.find("a").find('img')['alt'])
    runtimes.append(int(film.find(class_="runtime").get_text()[0:-3]))
    ratings.append(float(film.find(class_="ipl-rating-star__rating").get_text()))
    years.append(int(film.find(class_="lister-item-year text-muted unbold").get_text()[1:5]))


top100 = pd.DataFrame({
    "rank": ranks,
    "title": titles,
    "year": years,
    "rating": ratings,
    "runtime (min)": runtimes})

first50 = top100[:50]
avg_rating_first50 = first50.rating.mean()
last50 = top100[50:]
avg_rating_last50 = last50.rating.mean()

over_2_hours = top100[top100["runtime (min)"] > 120]
earliest_film = top100[top100.year == top100.year.min()]
latest_film = top100[top100.year == top100.year.max()]
top_rated = top100[top100.rating == top100.rating.max()]

print(earliest_film.title)
print(latest_film.title)
print(top_rated.title)
print(len(over_2_hours.title))
print(avg_rating_first50)
print(avg_rating_last50)

plt.figure(1)
plt.hist(top100.year)
plt.show(block=False)

plt.figure(2)
plt.plot(ranks, ratings, '.')
plt.show()
