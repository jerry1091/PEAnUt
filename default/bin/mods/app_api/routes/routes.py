from flask import Response, Blueprint
# from app.core.utils.logging_utils import app_logger


app_default = Blueprint('app_default', __name__)


@app_default.route('/app_default', methods=['GET'])
def get_default():
    # app_logger.info("Recieved api call.")
    return Response("Ok", status=200, mimetype='text/plain')
