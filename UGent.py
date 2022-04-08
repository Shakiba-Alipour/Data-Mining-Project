from inspect import Parameter
import requests
from bs4 import BeautifulSoup
import BaseCrawler
import logging
import csv



logger = logging.getLogger(__file__)



class UGhent(BaseCrawler):

    Course_Page_Url = 'https://www.ugent.be/doctoralschools/en/doctoraltraining/courses'
    University = 'Ghent University'
    Abbreviation = 'UGhent'
    University_Homepage = 'https://www.ugent.be/en'
    
    outcomes = []
    prerequisites = []
    courseName = []
    description = []
    departments_links = []
    courses = []

    Scores = None
    References = None
    Professor_Homepage = None
    Projects = None
    course_count = None

    response = requests.get(Course_Page_Url)
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

        courses = []
        Department_Name = soup.find('h1', class_ = 'documentFirstHeading')
        Course_Homepage = soup.find('base').get('href')

        for row in table:
            if row.find('a') is not None:
                courses.append(row.find('a').get('href'))

        return courses, Department_Name, Course_Homepage


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


    #   save information
    def save_course_data(University, Abbreviation, Department_Name, Course_Title, Unit_Count,
                    Professor, Objective, prerequisites, Required_Skills, Outcome, References, Scores,
                    Description, Projects, University_Homepage, Course_Homepage, Professor_Homepage):

        class UGhent(BaseCrawler):
            with open(Abbreviation + '.csv') as file:
                writer = csv.writer(file)
                writer.writerow(University)
                writer.writerow('Department Name: ' + Department_Name)
                writer.writerow('Course Title: ' + Course_Title)
                writer.writerow('Unit Count: ' + Unit_Count)
                writer.writerow('Profesor: ' + Professor)
                writer.writerow('Objectives: ' + Objective)
                writer.writerow('Prerequisites: ' + prerequisites)
                writer.writerow('Required Skills: ' + Required_Skills)
                writer.writerow('Outcome: ' + Outcome)
                writer.writerow('References: ' + References)
                writer.writerow('Scores: ' + Scores)
                writer.writerow('Description: ' + Description)
                writer.writerow('Projects: ' + Projects)
                writer.writerow('University Homepage: ' + University_Homepage)
                writer.writerow('Course Homepage: ' + Course_Homepage)
                writer.writerow('Profesor Homepage: ' + Professor_Homepage)


    #   handler
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
                    Professor, Objective, self.prerequisites, Required_Skills, Outcome, self.References, self.Scores,
                    Description, self.Projects, self.University_Homepage, Course_Homepage, self.Professor_Homepage
                )

            logger.info(f"{self.Abbreviation}: {Department_Name} department's data was crawled successfully.")

        logger.info(f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")