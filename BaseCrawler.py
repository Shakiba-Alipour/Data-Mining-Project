import csv
import logging

logger = logging.getLogger('__main__')


class BaseCrawler:
    Course_Page_Url = None
    University = None
    Abbreviation = None
    University_Homepage = None

    output_file = None
    course_count = 0

    def __init__(self):
        self.output_file = csv.writer(
            open(f'{self.__class__.__name__}.csv', 'w', encoding='utf-8', newline=''))
        self.output_file.writerow(
            ['University', 'Abbreviation', 'Department', 'Course title', 'Unit', 'Professor', 'Objective',
             'Prerequisite', 'Required Skills', 'Language', 'References', 'Scores', 'Description', 'Projects',
             'University Homepage', 'Course Homepage', 'Professor Homepage']
        )

    def get_departments(self):
        ...

    def get_courses_of_department(self, department):
        ...

    def get_course_data(self):
        ...

    def save_course_data(self, university, abbreviation, department_name, course_title, unit_count, professor,
                         objective, prerequisite, required_skills, language, references, scores, description, projects,
                         university_homepage, professor_homepage):
        try:
            self.output_file.writerow([university, abbreviation, department_name, course_title, unit_count, professor,
                                       objective, prerequisite, required_skills, language, references, scores,
                                       description, projects, university_homepage, professor_homepage])

            self.course_count += 1
        except Exception as e:
            logger.error(
                f"{abbreviation} - {department_name} - {course_title}: An error occurred while saving course data: {e}"
            )

    def handler(self):
        ...
