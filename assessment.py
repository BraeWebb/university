from database import database
from course import Course

class Assessment(object):
    def __init__(self, assessment_id):
        self.assessment_id = int(assessment_id)
        with database() as db:
            if db.exists('assessments', assessment_id = self.assessment_id):
                self.title, self.worth, self.due, self.course, self.result, self.done = \
                    db.query('SELECT title, worth, due, course, result, done FROM assessments WHERE assessment_id = %s', self.assessment_id)[0]

    @staticmethod
    def get_all(semester='2016S2'):
        with database() as db:
            if not semester:
                return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments')])
            else:
                return sorted([Assessment(assess[0]) for assess in db.query('SELECT assessment_id FROM assessments WHERE course IN (SELECT course FROM courses WHERE semester = %s)', semester)])

    @staticmethod
    def get_nocategory(semester='2016S2', done=True):
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

    def get_done(self):
        return self.done

    def __lt__(self, other):
        return self.get_due() < other.get_due()