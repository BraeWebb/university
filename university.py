from flask import Flask, render_template, request, redirect, url_for, jsonify

from assessment import Assessment
from category import Category
from course import Course

app = Flask(__name__)


@app.route('/assessments')
def view_assessments():
    return render_template('assessments.html', items=sorted(Category.get_all() + Assessment.get_nocategory()))

@app.route('/assessment/add')
def add_assessment():
    return render_template('add_assessment.html', courses=Course.get_all(), categories=[{'category_id': '', 'title': ''}]  + Category.get_all())

@app.route('/category/add')
def add_category():
    return render_template('add_category.html', courses=Course.get_all())

@app.route('/courses')
def view_courses():
    return render_template('courses.html', semesters=['2017S1', '2016S2', '2016S1'], Course=Course)

@app.route('/course/<course>')
def view_course(course):
    return render_template('course.html', course=Course(course))

@app.route('/course/add')
def add_course():
    return render_template('add_course.html')

@app.route('/assessment/<assessment_id>')
def view_assessment(assessment_id):
    return render_template('assessment.html', assessment=Assessment(assessment_id))

@app.route('/results')
def view_results():
    return 'A page containing many different statistics about assessment results'


# Jinja2 context and filters

@app.context_processor
def custom_context_utils():
    return dict(type_of=lambda item: type(item).__name__)

@app.template_filter('date')
def filter_date(date):
    # Credit to Acorn: http://stackoverflow.com/questions/5891555/display-the-date-like-may-5th-using-pythons-strftime
    suffix = 'th' if 11<=date.day<=13 else {1:'st',2:'nd',3:'rd'}.get(date.day%10, 'th')
    return date.strftime('%d{} of %B %Y').format(suffix).lstrip("0")


# API routes

@app.route('/api/assessment', methods=['POST'])
def api_add_assessment():
    attributes = [request.form.get('due'), request.form.get('title'), request.form.get('worth'), request.form.get('course')]
    due, title, worth, course, category = *attributes, request.form.get('category')
    if not all(bool(attr) for attr in attributes):
        return jsonify(**{'status': 'error', 'error':'Invalid Request', 'error_msg':'Not all required attributes were given'})
    try:
        assessment = Assessment.create(due, title, worth, course, category)
        return jsonify(**{'status':'success', 'assessment':{'id':assessment.get_id()}})
    except Exception as e:
        return jsonify(**{'status': 'error', 'error':type(e).__name__})

@app.route('/api/add/category', methods=['POST'])
def api_add_category():
    title, course = request.form.get('title'), request.form.get('course')
    category = Category.create(title, course)
    return redirect(url_for('view_assessments'))

@app.route('/api/add/course', methods=['POST'])
def api_add_course():
    course, title, semester, color = request.form.get('course'), request.form.get('title'), request.form.get('semester'), request.form.get('color')
    course = Course.create(course, title, semester, color)
    return redirect(url_for('view_courses'))

@app.route('/api/assessment/all')
def api_all_assessment():
    return jsonify(*[assessment.dict() for assessment in Assessment.get_all()])

@app.route('/api/assessment/<assessment_id>')
def api_assessment_detail(assessment_id):
    return jsonify(**Assessment(assessment_id).dict())

@app.route('/api/assessment/complete', methods=['POST'])
def api_complete_assessment():
    id = request.form.get('id')
    Assessment(id).set_done(True)
    return ''

@app.route('/api/assessment/grade', methods=['POST'])
def api_grade_assessment():
    id, result = request.form.get('id'), request.form.get('result')
    Assessment(id).set_result(result)
    return ''

@app.route('/api/assessment/delete', methods=['POST'])
def api_delete_assessment():
    id = request.form.get('id')
    Assessment(id).delete()
    return ''

@app.route('/api/category/delete', methods=['POST'])
def api_delete_category():
    id = request.form.get('id')
    Category(id).delete()
    return ''

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


if __name__ == '__main__':
    app.run(debug = True, use_reloader = True)
