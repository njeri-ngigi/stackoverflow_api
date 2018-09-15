'''./run.py'''
from flask import jsonify, render_template
from app.application import create_app

CONFIG_NAME = "development"
app = create_app(CONFIG_NAME)

@app.route('/')
def home():
    '''method to render documentation'''
    return render_template('documentation.html'), 200

if __name__ == "__main__":
    app.run()
    