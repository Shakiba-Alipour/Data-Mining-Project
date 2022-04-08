from inspect import Parameter
import requests
from bs4 import BeautifulSoup
import BaseCrawler
import logging

logger = logging.getLogger(__file__)



class UGhent(BaseCrawler):
    outcomes = []
    prerequisites = []
    courseName = []
    description = []
    departments_links = []
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

    #   find departments
    def get_departments(self, soup):
        department_element = soup.find_all('ul', id = 'parent-fieldname-text')
        departments = department_element.find_all('a')

        for department in departments:
            link = department.get('href')
            if link.endswith('.htm') is False:
                self.departments_links.append(link)

            
    #   find course links
    def get_courses_of_department(self, department):
        response = requests.get(department)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('tr')

        for row in table:
            if row.find('a') is not None:
                self.courses.append(row.find('a').get('href'))


    #   find informations of course
    def get_course_data(self, course):
        #course:
        #'https://www.ugent.be/doctoralschools/en/doctoraltraining/courses/specialistcourses/ahl/demystifying-chan-buddhism.htm'
        response = requests.get(course)
        soup = BeautifulSoup(response.content, 'html.parser')
        things = soup.find_all('h2')
        
        for thing in things:
            if thing.text == 'Objectives':
                self.objective = thing.next_element.next_element.next_element
                print(self.objective)
            else:
                if thing.text == 'Topic and Objectives':
                    self.objective = thing.next_element.next_element.next_element
                    print(self.objective)


    def handler(self):
        html_content = requests.get(self.Course_Page_Url).text
        soup = BeautifulSoup(html_content, 'html.parser')

        departments = soup.find(id='atozindex').find_all('li')
        for department in departments:
            courses, Department_Name, Course_Homepage = self.get_courses_of_department(department)
            for course in courses:
                Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description = self.get_course_data(
                    course)

                self.save_course_data(
                    self.University, self.Abbreviation, Department_Name, Course_Title, Unit_Count,
                    Professor, Objective, self.Prerequisite, Required_Skills, Outcome, self.References, self.Scores,
                    Description, self.Projects, self.University_Homepage, Course_Homepage, self.Professor_Homepage
                )

            logger.info(f"{self.Abbreviation}: {Department_Name} department's data was crawled successfully.")

        logger.info(f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")