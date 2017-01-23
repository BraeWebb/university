from database import database
from course import Course

class Assessment(object):
    def __init__(self, assessment_id):
        self.assessment_id = int(assessment_id)
        with database() as db:
            if db.exists('assessments', assessment_id = self.assessment_id):
                self.title, self.worth, self.due, self.course, self.result, self.done, self.category = \
                    db.query('SELECT title, worth, due, course, result, done, category FROM assessments WHERE assessment_id = %s', self.assessment_id)[0]

    @classmethod
    def create(cls, due, title, worth, course, category):
        with database() as db:
            id = db.query('SELECT MAX(assessment_id) FROM assessments')[0][0] + 1
            db.query('INSERT INTO assessments (assessment_id, title, worth, due, course, result, done, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                     id, title, worth, due, course, 0, False, category if category else None)
            return cls(id)

    def delete(self):
        with database() as db:
            db.query('DELETE FROM assessments WHERE assessment_id = %s', self.assessment_id)

    @staticmethod
    def get_all(semester='2017S1'):
        with database() as db:
            if not semester:
                return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments')])
            else:
                return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments WHERE course IN (SELECT course FROM courses WHERE semester = %s)', semester)])

    @staticmethod
    def get_nocategory(semester='2017S1', done=None):
        with database() as db:
            if done == None:
                if not semester:
                    return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments WHERE category IS NULL')])
                else:
                    return sorted([Assessment(assess[0])
                            for assess in db.query('SELECT assessment_id FROM assessments WHERE course IN (SELECT course FROM courses WHERE semester = %s) AND category IS NULL', semester)])
            else:
                if not semester:
                    return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments WHERE category IS NULL AND done = %s', done)])
                else:
                    return sorted([Assessment(assess[0])
                            for assess in db.query('SELECT assessment_id FROM assessments WHERE course IN (SELECT course FROM courses WHERE semester = %s) AND category IS NULL AND done = %s', semester, done)])


    def has_children(self):
        return False

    def get_id(self):
        return self.assessment_id

    def get_title(self):
        return self.title

    def get_worth(self):
        return self.worth

    def get_due(self):
        return self.due

    def get_course(self):
        return Course(self.course)

    def get_result(self):
        return self.result

    def set_result(self, result):
        with database() as db:
            db.query('UPDATE assessments SET result = %s WHERE assessment_id = %s', result, self.assessment_id)

    def get_done(self):
        return self.done

    def set_done(self, done):
        with database() as db:
            db.query('UPDATE assessments SET done = %s WHERE assessment_id = %s', done, self.assessment_id)

    def get_category(self):
        if self.category:
            from category import Category
            return Category(self.category)
        else:
            return None

    def dict(self):
        return {
            'id': self.assessment_id,
            'title': self.title,
            'worth': self.worth,
            'due': self.due,
            'course': self.course,
            'result': self.result,
            'done': self.result
        }

    def __lt__(self, other):
        return self.get_due() < other.get_due()