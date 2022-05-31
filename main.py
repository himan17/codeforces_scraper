from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
problemLinks = []
problemTitles = []

# This Scraper works on Codeforces Problem sets section.
# Just enter the no of problem set pages(range) you want to take. Each page has around 100 problems.
# Part 1 - For title and Link of urls
for i in range(1, 10):
    link = 'https://codeforces.com/problemset/page/'+str(i)
    driver.get(link)
    time.sleep(5)
    html = driver.page_source

    # creating soup for ps page
    soup = BeautifulSoup(html, 'html.parser')

    # Target div(All titles and links were in tr tag)
    problemTitleTr = soup.tbody.findAll('tr')

    for j in range(1, len(problemTitleTr)):
        problemTd = problemTitleTr[j].findAll('td')
        # 2nd td of tr has the problem title and link that too in its first div
        problemTdDiv = problemTd[1].div
        # optimising Problem titles
        problemTitlesString = problemTdDiv.a.text
        problemTitlesString = problemTitlesString.strip('\n')
        problemTitlesString = problemTitlesString.strip('  ')
        # optimising Problem links
        problemLinksString = 'https://codeforces.com'+problemTdDiv.a['href']
        problemLinks.append(problemLinksString)
        problemTitles.append(problemTitlesString)
    print(problemLinks)
    print(problemTitles)

# Saving them into file
with open('cfproblem_titles.txt', 'w+', encoding='utf-8') as f:
    f.write('\n'.join(problemTitles))
with open('cfproblem_links.txt', 'w+', encoding='utf-8') as f:
    f.write('\n'.join(problemLinks))

# Part 2 - Dealing With Problems( Extracting Problem statement from problem pages)
# Making Directory for Problems
mypath = 'C:\\Users\\himan\\PycharmProjects\\webscraperProject-CodeforcesPS\\cfproblems'
if not os.path.isdir(mypath):
    os.makedirs(mypath)

pCount = 521
for link in problemLinks:
    driver.get(link)
    time.sleep(5)
    html2 = driver.page_source

    soup2 = BeautifulSoup(html2, 'html.parser')

    problemStatement = []
    # Prevention if Page does not exist or different structure(VIMP: Few problems were in pdf format on cf)
    if not soup2.find('div', {"class": "problem-statement"}):
        problemStatement.append("Error Loading Problem")
    else:
        problemStatementDiv = soup2.find('div', {"class": "problem-statement"}).children
        i = 0
        for child in problemStatementDiv:
            if i > 0:
                problemStatement.append(child.text)
            i = i+1
    print(problemStatement)
    # Saving Problem into files at the Problem Directory
    # Encoding set to UTF8
    with open(os.path.join(mypath, 'cfproblem' + str(pCount) + '.txt'), 'w+', encoding='utf-8') as f:
        f.write('\n'.join(problemStatement))
    pCount = pCount + 1
