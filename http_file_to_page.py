"""Flask application."""

from traceback import extract_tb

from flask import Flask, jsonify, request
from flask_api import exceptions as flask_errors, status
from werkzeug import exceptions as werkzeug_errors

import const
from file_to_page.pretty_html import PrettyHTML

app = Flask(__name__)
prettyhtml = PrettyHTML()


@app.errorhandler(404)
def handle_404(err: 'werkzeug_errors.NotFound'):
    """Handle not found."""
    err_message = str(err)
    result = {"error": err_message}
    app.logger.error(f"error = {err_message}")
    return jsonify(result), status.HTTP_404_NOT_FOUND


@app.errorhandler(405)
def handle_405(err: 'werkzeug_errors.MethodNotAllowed'):
    """Handle not allowed methods' exceptions."""
    result = {
        "error": f"{request.method} is not allowed",
        "valid methods": ",".join(err.valid_methods),
    }
    app.logger.error(f"{request.method} is not allowed, error = {str(err)}")
    return jsonify(result), status.HTTP_405_METHOD_NOT_ALLOWED


@app.errorhandler(Exception)
def unhandled_exceptions(e):
    """Handle any other exception."""
    exception = e.__repr__()
    tb_info = "\n".join([str(x) for x in extract_tb(e.__traceback__)])
    app.logger.error(f"Unhandled Exception: {exception}")
    app.logger.error(f"traceback: {tb_info}")

    if isinstance(e, werkzeug_errors.HTTPException):
        result = {"error": e.description}
        code = e.code
    elif isinstance(e, flask_errors.APIException):
        result = {"error": e.detail}
        code = e.status_code
    else:
        result = {"error": "an error has occurred"}
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
    result["code"] = code
    return jsonify(result), code


@app.route("/", defaults={'file_name': const.FILE_DEFAULT}, methods=["GET"])
@app.route("/<string:file_name>", methods=["GET"])
def get_page_from_file(file_name: str) -> str:
    """Takes an HTML file name. If exists returns an HTML page with a prettified
    content. The query parameters "start" and "stop" can be used to specify the
    start and end line numbers.
    """
    start = request.args.get(const.URL_QUERY_START, type=int)
    stop = request.args.get(const.URL_QUERY_STOP, type=int)
    return prettyhtml.get_html(const.FILE_PATH / f'{file_name}', start, stop)


if __name__ == "__main__":
    app.run(debug=const.WEB_SERVER_DEBUG)
