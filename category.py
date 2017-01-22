from database import database
from assessment import Assessment
from course import Course
from datetime import datetime

class Category(object):
    def __init__(self, category_id):
        self.category_id = category_id
        with database() as db:
            if db.exists('categories', category_id = self.category_id):
                self.course, self.title = \
                    db.query('SELECT course, title FROM categories WHERE category_id = %s', self.category_id)[0]
                if db.exists('assessments', category = self.category_id):
                    self.worth = db.query('SELECT SUM(worth) FROM assessments WHERE category = %s', self.category_id)[0][0]
                    self.done = not db.exists('assessments', category = self.category_id, done = False)
                    self.result = db.query('SELECT SUM(result*worth) FROM assessments WHERE category = %s', self.category_id)[0][0]/self.worth
                    if not self.done:
                        self.due = db.query('SELECT MIN(due) FROM assessments WHERE category = %s AND not done', self.category_id)[0][0]
                    else:
                        self.due = db.query('SELECT MAX(due) FROM assessments WHERE category = %s', self.category_id)[0][0]
                else:
                    self.result, self.done, self.worth = 0, 0, 0
                    self.due = datetime.date(datetime.now())

    @classmethod
    def create(cls, title, course):
        with database() as db:
            id = db.query('SELECT MAX(category_id) FROM categories')[0][0] + 1
            db.query(
                'INSERT INTO categories (category_id, title, course) VALUES (%s, %s, %s)',
                id, title, course)
            return cls(id)

    def delete(self):
        with database() as db:
            db.query('DELETE FROM categories WHERE category_id = %s', self.category_id)

    @staticmethod
    def get_all(semester='2017S1'):
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

    def get_result(self):
        return self.result

    def get_done(self):
        return self.done

    def get_assessment(self, done=None):
        with database() as db:
            if done == None:
                return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments WHERE category = %s', self.category_id)])
            else:
                return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments WHERE category = %s AND done = %s', self.category_id, done)])

    def __lt__(self, other):
        return self.get_due() < self.get_due()

    def __repr__(self):
        return 'Category #{}: {}'.format(self.category_id, self.title)