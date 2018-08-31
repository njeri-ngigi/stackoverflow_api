'''./run.py'''
from app import createApp
from flask import jsonify

config_name = "development"
app = createApp(config_name)

'''Error handlers'''
@app.errorhandler(400)
def bad_request(error):
    '''Bad request'''
    return jsonify(dict(error = 'Bad request')), 400
@app.errorhandler(404)
def page_not_found(error):
    '''Page not found'''
    return jsonify(dict(error = 'Page not found')), 404

@app.errorhandler(405)
def unauthorized_method(error):
    '''Unauthorized method'''
    return jsonify(dict(error = 'Method not allowed')), 405

@app.errorhandler(500)
def server_error(error):
    '''Internal server error'''
    return jsonify(dict(error = 'Internal server error')), 500

if __name__ == "__main__":
    app.run()