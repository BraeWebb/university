from flask import Flask, render_template

from assessment import Assessment, Category

app = Flask(__name__)


@app.route('/assessments')
def view_assessments():
    return render_template('assessments.html', grouping=sorted(Category.get_all() + Assessment.get_nocategory()))

@app.route('/results')
def view_results():
    return 'A page containing many different statistics about assessment results'

@app.context_processor
def custom_context_utils():
    return dict(type_of=lambda item: type(item).__name__)


if __name__ == '__main__':
    app.run()
