from flask import Flask, render_template, request

from assessment import Assessment, Category
from course import Course

app = Flask(__name__)


@app.route('/assessments')
def view_assessments():
    return render_template('assessments.html', grouping=sorted(Category.get_all() + Assessment.get_nocategory()))

@app.route('/assessment/<assessment_id>')
def view_assessment(assessment_id):
    return render_template('assessment.html', assessment=Assessment(assessment_id))

@app.route('/assessment/add')
def add_assessment():
    return render_template('add_assessment.html', courses=Course.get_all(), categories=[{'category_id': '', 'title': ''}]  + Category.get_all())

@app.route('/category/add')
def add_category():
    return render_template('add_category.html', courses=Course.get_all())

@app.route('/results')
def view_results():
    return 'A page containing many different statistics about assessment results'

@app.route('/courses')
def view_courses():
    return render_template('courses.html', semesters=['2017S1', '2016S2', '2016S1'], Course=Course)

@app.route('/course/<course>')
def view_course(course):
    return render_template('course.html', course=Course(course))

@app.route('/course/add')
def add_course():
    return render_template('add_course.html')

@app.route('/api/course/delete', methods=['POST'])
def api_delete_course():
    id = request.form.get('id')
    Course(id).delete()
    return ''

@app.route('/api/course/edit', methods=['POST'])
def api_edit_course():
    id = request.form.get('id')
    title, semester, color = request.form.get('title'), request.form.get('semester'), request.form.get('color')
    course = Course(id)
    print(color)
    if title:
        course.set_title(title)
    if semester:
        course.set_semester(semester)
    if color or color == 0:
        course.set_color(color)
    return ''

@app.context_processor
def custom_context_utils():
    return dict(type_of=lambda item: type(item).__name__)


if __name__ == '__main__':
    app.run()