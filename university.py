from flask import Flask

app = Flask(__name__)


@app.route('/assessments')
def view_assessments():
    return 'An index of assessments with information regarding their completion, work, due date, course and result'

@app.route('/results')
def view_results():
    return 'A page containing many different statistics about assessment results'


if __name__ == '__main__':
    app.run()
