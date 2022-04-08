from inspect import Parameter
import requests
from bs4 import BeautifulSoup
import BaseCrawler

outcomes = []
prerequisites = []
courseName = []
description = []
links = []
courses = []

# response = requests.get('https://www.rug.nl/ocasys/rug/main/browseByFaculty')

# soup = BeautifulSoup(response.content, 'html.parser')

# subjects_element = soup.find(class_="main") 

# subjects = subjects_element.find_all('li')

# for subject in subjects:
#     link = 'https://www.rug.nl/ocasys/rug' + subject.find('a', id="nodeNotSelected").get('href')[2:]
#     res = requests.get(link)
#     soup = BeautifulSoup(res.content, 'html.parser')
#     courses_element = soup.find(class_="userTable")
#     courses_name = courses_element.find_all('td')

#     for course in courses_name:
#         courseLink = course.find('a')
        
#         if courseLink != None:
#             course_Link = 'https://www.rug.nl' + course.find('a').get('href')
#             course_res = requests.get(course_Link)
#             soup = BeautifulSoup(course_res.content, 'html.parser')
#             detail = soup.find(class_="detailTable")
#             details_name = detail.find_all('tr')

#             for detail_name in details_name:
#                 data = detail_name.find('td', class_='fieldLabel')                  # find title of datas 
                
#                 if data != None:
#                     if data.text == 'Leerdoelen':                                   # find Learning outcomes
#                         outcomes.append(data.findNext('td').text.strip())           # Add datas to outcomes array 

#                     if data.text == 'Entreevoorwaarden':                            # find Prerequisites
#                         prerequisites.append(data.findNext('td').text.strip())      # Add datas to Prerequisites array 
                        
#                     if data.text == 'Uitgebreide vaknaam':                          # find course name
#                         courseName.append(data.findNext('td').text.strip())         # Add datas to courseName array 
                        
#                     if data.text == 'Omschrijving':                                 # find overview
#                         description.append(data.findNext('td').text.strip())        # Add datas to description array 

#                     print(data.findNext('td').text.strip())


response = requests.get('https://www.ugent.be/doctoralschools/en/doctoraltraining/courses')
soup = BeautifulSoup(response.content, 'html.parser')

#    find departments
def get_departments(soup):
    department_element = soup.find_all('ul', id = 'parent-fieldname-text')
    departments = department_element.find_all('a')

    for department in departments:
        link = department.get('href')
        if link.endswith('.htm') is False:
            links.append(link)

        
#   find course links
    
response = requests.get(links[0])
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find_all('tr')
for row in table:
    if row.find('a') is not None:
        courses.append(row.find('a').get('href'))

#   find informations of course

response = requests.get('https://www.ugent.be/doctoralschools/en/doctoraltraining/courses/specialistcourses/ahl/demystifying-chan-buddhism.htm')
soup = BeautifulSoup(response.content, 'html.parser')
things = soup.find_all('h2')
for thing in things:
    if thing.text == 'Objectives':
        objective = thing.next_element.next_element.next_element
        print(objective)
    else:
        if thing.text == 'Topic and Objectives':
            objective = thing.next_element.next_element.next_element
            print(objective)
#print(things)
