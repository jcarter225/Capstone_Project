"""
Justin Carter
Script to scrape NCAA Football Scores of Week 5

This script is designed to get the final scores and the teams
that played in week 5 of 2022.

"""


import requests
from bs4 import BeautifulSoup
import pandas as pd

Outcomes_response = requests.get('https://www.cbssports.com/college-football/scoreboard/FBS/2022/regular/5/', 'html.parser')

Outcomes_webpage = Outcomes_response.content

Outcomes_soup = BeautifulSoup(Outcomes_webpage)


#Get all elements of soup object that have class team
Outcomes_list = Outcomes_soup.find_all(attrs = {'class': 'team team--collegefootball'})


#get text contained within the tags and strip whitespace
Outcomes_element_list = []
for element in Outcomes_list:
    element = str(element.get_text('|'))
    element = element.strip()
    element = element.split('|')
    Outcomes_element_list.append(element)
    
#separated elements with the slash. Now need to put them in list and get rid of nums in list

nope_lst = ['0','1','2','3','4','5','6','7','8','9','10', ' ']
    
#get out of list of lists
Outcomes_element_lst = []
for sublst in Outcomes_element_list:
    for ele in sublst:
        if ele[0] in nope_lst:
            continue
        else:
            Outcomes_element_lst.append(ele)
        

# got all the teams names I need.

#now will get all final scores
    
#==================================================

Outcomes_total_scores_list = Outcomes_soup.find_all(attrs = {'class': 'total-score'})



#make initial list of team names and scores
Outcomes_total_scores_element_list = []
for element in Outcomes_soup.find_all('tr'):
    element = str(element.get_text('|'))
    element = element.strip()
    element = element.split('|')
    Outcomes_total_scores_element_list.append(element)
    
    
#get lines of teams and scores isolated and cleaned
Outcomes_total_scores_element_lst = []
for sublist in Outcomes_total_scores_element_list:
    if sublist[-1]=="T" or sublist[-1] =="More College Football News":
        continue
    else:
        Outcomes_total_scores_element_lst.append(sublist)
    
    
#take the last element of each sublist, which is the 
#final score:
scores_list = []
for sublist in Outcomes_total_scores_element_lst:
    scores_list.append(sublist[-1])


# make data frame and split lists to be put into columns

my_df = pd.DataFrame()


away_teams = Outcomes_element_lst[::2]
home_teams = Outcomes_element_lst[1::2]
away_team_total_scores = scores_list[::2]
home_team_total_scores = scores_list[1::2]

my_df["Away_Team"] = away_teams
my_df["Home_Team"] = home_teams
my_df["Away_Team_Total_Score"] = away_team_total_scores
my_df["Home_Team_Total_Score"] = home_team_total_scores


#make all variables strings to avoid confusing Excel
Outcomes_df = my_df.astype(str)

#make csv file
Outcomes_df.to_csv("Week5GameOutcomes.csv")


