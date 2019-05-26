from flask import Response, Blueprint
# from app.core.utils.logging_utils import app_logger


default = Blueprint('default', __name__)


@default.route('/health', methods=['GET'])
def get_health():
    # app_logger.info("Recieved api call.")
    return Response("Ok", status=200, mimetype='text/plain')
