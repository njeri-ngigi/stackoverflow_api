'''./run.py'''
from flask import jsonify, render_template
from app.application import create_app

CONFIG_NAME = "development"
app = create_app(CONFIG_NAME)

'''Error handlers'''
@app.errorhandler(400)
def bad_request(_error):
    '''Bad request'''
    return jsonify(dict(error='Bad request')), 400
@app.errorhandler(404)
def page_not_found(_error):
    '''Page not found'''
    return jsonify(dict(error='Page not found')), 404
@app.errorhandler(500)
def internal_server_error(_error):
    '''Internal server error'''
    return jsonify(dict(error='Internal server error')), 500
@app.errorhandler(405)
def unauthorized_method(_error):
    '''Unauthorized method'''
    return jsonify(dict(error='Method not allowed')), 405

@app.route('/')
def home():
    '''method to render documentation'''
    return render_template('documentation.html'), 200

if __name__ == "__main__":
    app.run()
    