import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import unicodedata
import re
import csv
import json

page_limit = 9999
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
score_pattern = re.compile(r'(\s\d{1,3}[\-]\d{1,3}\s)')
# ================ Task 3 setup ================ #
task3 = open("task3.csv", 'w', newline='')
task3_writer = csv.writer(task3)
task3_writer.writerow(["team", "avg game difference"])
game_difference = {}
# ================ Task 4 setup ================ #


# Specify the initial page to crawl
base_url = 'http://comp20008-jh.eng.unimelb.edu.au:9889/main/'
seed_item = 'index.html'

seed_url = base_url + seed_item
page = requests.get(seed_url)
soup = BeautifulSoup(page.text, 'html.parser')

visited = {};
visited[seed_url] = True
pages_visited = 1
print(seed_url)

# Remove index.html
links = soup.findAll('a')
seed_link = soup.findAll('a', href=re.compile("^index.html"))
# to_visit_relative = list(set(links) - set(seed_link))
to_visit_relative = [l for l in links if l not in seed_link]

# Resolve to absolute urls
to_visit = []
for link in to_visit_relative:
    to_visit.append(urljoin(seed_url, link['href']))

# Find all outbound links on successor pages and explore each one
while (to_visit):
    # Impose a limit to avoid breaking the site
    if pages_visited == page_limit:
        break

    # consume the list of urls
    link = to_visit.pop(0)

    # need to concat with base_url, an example item <a href="catalogue/sharp-objects_997/index.html">
    page = requests.get(link)

    # scarping code goes here
    soup = BeautifulSoup(page.text, 'html.parser')

    # ================ Task 1 scarping ================ #
    headline = soup.find("h1", class_="headline").text
    task1_writer.writerow([link, headline])
    # ================ Task 2 scarping ================ #
    text = headline
    # convert webpage into a string
    text_list = soup.findAll('p')
    for paragraph in text_list:
        text = text + " " + paragraph.text
    # find the first appeared team name
    last_team_index = -1
    first_mentioned_team = ''
    for team in team_name:
        index = text.find(team)
        if index != -1 and (index < last_team_index or last_team_index == -1):
            first_mentioned_team = team
            last_team_index = index
    # find all scores
    result = score_pattern.findall(text)
    # find the best score for team 1
    best_team1_score = -1
    for score in result:
        cur_team1_score = int(score[1:score.find('-')])
        if cur_team1_score > best_team1_score:
            best_team1_score = cur_team1_score
    print(best_team1_score)
    # if a team is mentioned and scored
    if first_mentioned_team != '' and best_team1_score != -1:
        task2_writer.writerow([link, headline, first_mentioned_team, best_team1_score])
    # ================ Task 3 scarping ================ #
    if first_mentioned_team != '' and len(result) > 0:
        if first_mentioned_team not in game_difference:
            game_difference[first_mentioned_team] = [0, 0]
        for score in result:
            t1 = int(score[1:score.find('-')])
            t2 = int(score[score.find('-') + 1:-1])
            game_difference[first_mentioned_team][0] += abs(t1 - t2)
            game_difference[first_mentioned_team][1] += 1


    # mark the item as visited, i.e., add to visited list, remove from to_visit
    visited[link] = True
    to_visit
    new_links = soup.findAll('a')
    for new_link in new_links:
        new_item = new_link['href']
        new_url = urljoin(link, new_item)
        if new_url not in visited and new_url not in to_visit:
            to_visit.append(new_url)

    pages_visited = pages_visited + 1

for team in game_difference:
    avg_dif = game_difference[team][0] / game_difference[team][1]
    task3_writer.writerow([team, avg_dif])

print('\nvisited {0:5d} pages; {1:5d} pages in to_visit'.format(len(visited), len(to_visit)))
# print('{0:1d}'.format(pages_visited))
