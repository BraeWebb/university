from database import database


class Course(object):
    """
    Course representing a university course identified by a course code with title, semester taken and color
    information
    """

    def __init__(self, course):
        """
        Gather course attributes from that database based on the course code
        If the course doesn't exist raises ValueError
        """
        self.course = course
        with database() as db:
            if db.exists('courses', course=self.course):
                sql = 'SELECT title, semester, color FROM courses WHERE course = %s'
                self.title, self.semester, self.color = db.query(sql, self.course)[0]
            else:
                raise ValueError('No course exists within the database with course code {}'.format(self.course))

    @classmethod
    def create(cls, course, title, semester, color):
        """Create a course within the database with the given course code and attributes"""
        with database() as db:
            sql = 'INSERT INTO courses (course, title, semester, color) VALUES (%s, %s, %s, %s)'
            db.query(sql, course, title, semester, color)
        return cls(course)

    def delete(self):
        """Delete the course from the database"""
        with database() as db:
            db.query('DELETE FROM courses WHERE course = %s', self.course)

    @staticmethod
    def get_all(semester='2017S1'):
        """
        If semester is None retrieves all courses from the database
        Otherwise retrieve all courses with the matching semester attribute
        """
        with database() as db:
            if not semester:
                return [Course(course[0]) for course in db.query('SELECT course FROM courses')]
            else:
                sql = 'SELECT course FROM courses WHERE semester = %s'
                return [Course(course[0]) for course in db.query(sql, semester)]

    def get_assessments(self):
        """Retrieve a list of all assessments associated with the course"""
        from assessment import Assessment
        with database() as db:
            sql = 'SELECT * FROM assessments WHERE course = %s'
            return [Assessment(assessment[0]) for assessment in db.query(sql, self.course)]

    def get_id(self):
        """Return the course code of the course instance"""
        return self.course

    def get_title(self):
        """Return the title of the course"""
        return self.title

    def get_semester(self):
        """Return the semester the course is taken in"""
        return self.semester

    def get_color(self):
        """Return the bootstrap color label based on the color of the course"""
        list = ['info', 'success', 'danger', 'warning']
        return list[self.color]
