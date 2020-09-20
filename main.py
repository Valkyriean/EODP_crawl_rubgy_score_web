# code adopted from week 5's workshop
# modified by Jiachen Li, 1068299
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import matplotlib.pyplot as plt
import re
import csv
import json

# ================ Task 1 setup ================ #
task1 = open("task1.csv", 'w', newline='')
task1_writer = csv.writer(task1)
task1_writer.writerow(["url", "headline"])

# ================ Task 2 setup ================ #
task2 = open("task2.csv", 'w', newline='')
task2_writer = csv.writer(task2)
task2_writer.writerow(["url", "headline", "team", "score"])
rugby_file = open("rugby.json")
rugby = json.load(rugby_file)
team_name = []
for team in rugby.get("teams"):
    team_name.append(team.get('name'))
score_pattern = re.compile(r'(\s\d{1,3}[\-]\d{1,3})')
# ================ Task 3 setup ================ #
task3 = open("task3.csv", 'w', newline='')
task3_writer = csv.writer(task3)
task3_writer.writerow(["team", "avg_game_difference"])
game_difference = {}
# ================ Task 4 setup ================ #
mention_freq = {}
for name in team_name:
    mention_freq[name] = 0

# Specify the initial page to crawl
base_url = 'http://comp20008-jh.eng.unimelb.edu.au:9889/main/'
seed_item = 'index.html'

seed_url = base_url + seed_item
page = requests.get(seed_url)
soup = BeautifulSoup(page.text, 'html.parser')

visited = {seed_url: True}
pages_visited = 1
print(seed_url)

# Remove index.html
links = soup.findAll('a')
seed_link = soup.findAll('a', href=re.compile("^index.html"))
to_visit_relative = [l for l in links if l not in seed_link]

# Resolve to absolute urls
to_visit = []
for link in to_visit_relative:
    to_visit.append(urljoin(seed_url, link['href']))

# Find all outbound links on successor pages and explore each one
while to_visit:
    # consume the list of urls
    link = to_visit.pop(0)
    # need to concat with base_url, an example item <a href="catalogue/sharp-objects_997/index.html">
    page = requests.get(link)
    # scarping start from here
    soup = BeautifulSoup(page.text, 'html.parser')
    # ================ Task 1 scarping ================ #
    headline = soup.find("h1", class_="headline").text
    task1_writer.writerow([link, headline])
    # ================ Task 2 scarping ================ #
    # convert webpage into a string
    article = headline
    text_list = soup.findAll('p')
    for paragraph in text_list:
        article = article + " " + paragraph.text
    # find the first appeared team name
    last_team_index = -1
    first_mentioned_team = ''
    for team in team_name:
        index = article.find(team)
        if index != -1 and (index < last_team_index or last_team_index == -1):
            first_mentioned_team = team
            last_team_index = index
    # save all scores appeared in webpage
    results = score_pattern.findall(article)
    # find the best score for team 1
    largest_match_score = ""
    largest_sum = -1
    difference = -1
    # if the page is considered valid with team name and score
    if first_mentioned_team != '' and len(results) > 0:
        # increase the mention frequency counter by one
        mention_freq[first_mentioned_team] = mention_freq[first_mentioned_team] + 1
        for score in results:
            score = re.sub('\s', '', score)
            # extract two scores
            t1 = int(score[0:score.find('-')])
            t2 = int(score[score.find('-') + 1:len(score)])
            # task 2
            if t1 + t2 > largest_sum:
                largest_match_score = score
                largest_sum = t1 + t2
                difference = abs(t1 - t2)
            # task 3
        if first_mentioned_team not in game_difference:
            game_difference[first_mentioned_team] = [0, 0]
        game_difference[first_mentioned_team][0] += difference
        game_difference[first_mentioned_team][1] += 1
        task2_writer.writerow([link, headline, first_mentioned_team, largest_match_score])

    # mark the item as visited, i.e., add to visited list, remove from to_visit
    visited[link] = True
    new_links = soup.findAll('a')
    for new_link in new_links:
        new_item = new_link['href']
        new_url = urljoin(link, new_item)
        if new_url not in visited and new_url not in to_visit:
            to_visit.append(new_url)

    pages_visited = pages_visited + 1

# calculate average game score difference
for team in game_difference:
    avg_dif = game_difference[team][0] / game_difference[team][1]
    task3_writer.writerow([team, avg_dif])
    game_difference[team] = avg_dif

# Task 4 plot
mention_freq_series = pd.Series(mention_freq)
frequency_data = pd.DataFrame({'frequency': mention_freq_series})
frequency_data = frequency_data.sort_values(by='frequency', ascending=False).head(5)
plt.xticks(rotation='vertical')
plt.bar(frequency_data.index, frequency_data['frequency'])
plt.xlabel('Team name')
plt.ylabel('Mentioned frequency')
plt.title("Task 4")
plt.savefig("task4.png", bbox_inches='tight')
plt.clf()
# Task 5 plot
game_difference_series = pd.Series(game_difference)
frequency_score_data = pd.DataFrame({'frequency':mention_freq_series , 'score difference':game_difference_series})
plt.scatter(frequency_score_data['frequency'], frequency_score_data['score difference'])
plt.xlabel('Mentioned frequency')
plt.ylabel('fame_difference')
plt.title("Task 5")
plt.savefig("task5.png", bbox_inches='tight')

print('\nvisited {0:5d} pages; {1:5d} pages in to_visit'.format(len(visited), len(to_visit)))