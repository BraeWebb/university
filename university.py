from flask import Flask, render_template

from assessment import Assessment, Category
from course import Course

app = Flask(__name__)


@app.route('/assessments')
def view_assessments():
    return render_template('assessments.html', grouping=sorted(Category.get_all() + Assessment.get_nocategory()))

@app.route('/results')
def view_results():
    return 'A page containing many different statistics about assessment results'

@app.route('/courses')
def view_courses():
    return render_template('courses.html', semesters=['2017S1', '2016S2', '2016S1'], Course=Course)

@app.route('/course/<course>')
def view_course(course):
    return render_template('course.html', course=Course(course))

@app.context_processor
def custom_context_utils():
    return dict(type_of=lambda item: type(item).__name__)


if __name__ == '__main__':
    app.run()