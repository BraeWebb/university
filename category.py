from database import database
from assessment import Assessment
from course import Course

class Category(object):
    def __init__(self, category_id):
        self.category_id = category_id
        with database() as db:
            if db.exists('categories', category_id = self.category_id):
                self.course, self.title = \
                    db.query('SELECT course, title FROM categories WHERE category_id = %s', self.category_id)[0]
                self.worth = db.query('SELECT SUM(worth) FROM assessments WHERE category = %s', self.category_id)[0][0]
                self.due = db.query('SELECT MIN(due) FROM assessments WHERE category = %s', self.category_id)[0][0]

    @staticmethod
    def get_all(semester='2016S2'):
        with database() as db:
            if not semester:
                return [Category(cat[0]) for cat in db.query('SELECT category_id FROM categories')]
            else:
                return [Category(cat[0]) for cat in db.query('SELECT category_id FROM categories WHERE course IN (SELECT course FROM courses WHERE semester = %s)', semester)]

    def get_id(self):
        return self.category_id

    def get_course(self):
        return Course(self.course)

    def get_title(self):
        return self.title

    def get_worth(self):
        return self.worth

    def get_due(self):
        return self.due

    def get_assessment(self, done=True):
        with database() as db:
            return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments WHERE category = %s AND done = %s', self.category_id, done)])

    def __lt__(self, other):
        return self.get_due() < self.get_due()