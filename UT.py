import logging
import requests
from bs4 import BeautifulSoup
import requests
import csv
import selenium
from selenium import webdriver
import selenium.webdriver.chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from BaseCrawler import BaseCrawler


logger = logging.getLogger(__file__)


class UT(BaseCrawler):

    Course_Page_Url = 'https://osiris.utwente.nl/student/SetTaal.do?taal=en&bronUrl=/OnderwijsCatalogusZoekCursus.do&event=setTaal&requestToken=6f2bae755c8b9fdb99ffc1f749d5760abb66eb5f'
    University = 'University of Twente'
    Abbreviation = 'UT'
    University_Homepage = 'https://www.utwente.nl/en/'

    content = []
    selects = []
    aims = []
    required_materials = []
    courseNames = []
    lecturers = []
    language_of_instructions = []
    faculty_element = []

    Scores = ''
    References = ''
    Professor_Homepage = ''
    Projects = ''
    course_count = ''
    prerequisites = ''

    driver = webdriver.Chrome()
    driver.get(Course_Page_Url)
    response = requests.get(Course_Page_Url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find course links
    def get_courses_of_department(self, department):
        path = "//select[@name='faculteit']/option[text()='" + \
            department + "']"
        self.driver.find_element_by_xpath(path).click()

        Department_Name = department

        return Department_Name

    # find informations of course
    def get_course_data(self):

        Course_Title = self.driver.find_element(
            by=By.XPATH, value='//*[@id="headerCursus"]/span[2]').text
        self.courseNames.append(Course_Title)

        Unit_Count = ''
        Outcome = ''
        Required_Skills = ''
        Description = ''
        prerequisites = ''

        language = self.driver.find_element_by_xpath(
            '//*[@id="cursVoertaal"]/td[3]/span').text
        self.language_of_instructions.append(language)

        lecturer = self.driver.find_element_by_id('OnderwijsCursusDocent').text
        self.lecturers.append(lecturer)

        aim = self.driver.find_element_by_xpath(
            '/html/body/form/table/tbody/tr/td/table[6]/tbody/tr[2]/td[1]/table[1]/tbody/tr/td/span/table[2]/tbody/tr[2]/td[2]/span/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/table[2]/tbody/tr/td').text
        self.aims.append(aim)

        return Course_Title, Unit_Count, aim, language, lecturer, Required_Skills, Description, prerequisites

    # handler
    def handler(self):
        html_content = requests.get(self.Course_Page_Url).text
        soup = BeautifulSoup(html_content, 'html.parser')

        # find faculties
        faculty_elements = soup.find("select", {"name": "faculteit"})
        for a in faculty_elements.find_all('option')[1:]:
            a = a.text.strip()
            self.faculty_element.append(a)
            Department_Name = self.get_courses_of_department(a)
            try:
                if self.driver.find_element_by_tag_name("table"):
                    for i in range(2, 32):
                        path = '//*[@id="OnderwijsZoekCursus"]/table/tbody/tr[2]/td/table/tbody/tr[ ' + str(
                            i) + ']/td[1]/a'
                        self.driver.find_element_by_xpath(path).click()

                        Course_Title, Unit_Count, Objective, language, Professor, Required_Skills, Description, prerequisites = self.get_course_data()

                        self.save_course_data(
                            self.University, self.Abbreviation, Department_Name, Course_Title, Unit_Count,
                            Professor, Objective, self.prerequisites, Required_Skills, language, self.References, self.Scores,
                            Description, self.Projects, self.University_Homepage, self.Professor_Homepage
                        )

                        self.driver.get(self.Course_Page_Url)
                        path = "//select[@name='faculteit']/option[text()='" + \
                            a + "']"
                        self.driver.find_element_by_xpath(path).click()
            except NoSuchElementException:
                continue

            logger.info(
                f"{self.Abbreviation}: {Department_Name} department's data was crawled successfully.")

        logger.info(
            f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")


crawler = UT()
crawler.handler()
