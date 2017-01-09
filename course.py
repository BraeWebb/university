from database import database

class Course(object):
    def __init__(self, course):
        self.course = course
        with database() as db:
            if db.exists('courses', course = self.course):
                self.title, self.semester, self.color = \
                    db.query('SELECT title, semester, color FROM courses WHERE course = %s', self.course)[0]
            else:
                self.title = 'HI'
                self.semester = '2016S2'
                self.color = 0

    def get_id(self):
        return self.course

    def get_title(self):
        return self.title

    def get_semester(self):
        return self.semester

    def get_color(self):
        list = ['info', 'success', 'danger', 'warning']
        return list[self.color]