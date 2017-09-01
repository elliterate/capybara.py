import flask
from flask import Flask, render_template, request
import json
import time


app = Flask(__name__)

# Ensure application exceptions are raised.
app.debug = True


class AppError(Exception):
    pass


@app.route("/")
def hello():
    resp = flask.make_response("""Hello world! <a href="with_html">Relative</a>""")
    resp.set_cookie("capybara", "root cookie")
    return resp


@app.route("/foo")
def foo():
    return "Another World"


@app.route("/redirect", methods=["GET", "POST"])
def redirect():
    return flask.redirect("/redirect_again")


@app.route("/redirect_again")
def redirect_again():
    return flask.redirect("/landed")


@app.route("/referrer_base")
def referrer_base():
    return """
    <a href="/get_referrer">direct link</a>
    <a href="/redirect_to_get_referrer">link via redirect</a>
    <form action="/get_referrer" method="get"><input type="submit"></form>
    """


@app.route("/redirect_to_get_referrer")
def redirect_to_get_referrer():
    return flask.redirect("/get_referrer")


@app.route("/get_referrer")
def get_referrer():
    return "No referrer" if request.referrer is None else "Got referrer: {0}".format(request.referrer)


@app.route("/host")
def host():
    return "Current host is {0}://{1}".format(request.scheme, request.host)


@app.route("/redirect/<int:times>/times")
def redirect_n_times(times):
    if times == 0:
        return "redirection complete"
    else:
        return flask.redirect("/redirect/{0}/times".format(times - 1))


@app.route("/landed")
def landed():
    return "You landed"


@app.route("/with-quotes")
def with_quotes():
    return "\"No,\" he said, \"you can't do that.\""


@app.route("/form/get", methods=["GET"])
@app.route("/relative", methods=["POST"])
@app.route("/form", methods=["POST"])
def results():
    data = request.args.copy()
    data.update(request.form)
    return """<pre id="results">""" + json.dumps(data.to_dict(flat=False)) + """</pre>"""


@app.route("/favicon.ico")
def favicon():
    return ""


@app.route("/delete", methods=["DELETE"])
def deleted():
    return "The requested object was deleted"


@app.route("/delete", methods=["GET"])
def not_deleted():
    return "Not deleted"


@app.route("/redirect_back")
def redirect_back():
    return flask.redirect(request.referrer)


@app.route("/redirect_secure")
def redirect_secure():
    return flask.redirect("http://{0}/host".format(request.host))


@app.route("/slow_response")
def slow_response():
    time.sleep(2)
    return "Finally!"


@app.route("/set_cookie")
def set_cookie():
    cookie_value = "test_cookie"
    resp = flask.make_response("Cookie set to {0}".format(cookie_value))
    resp.set_cookie("capybara", cookie_value)
    return resp


@app.route("/get_cookie")
def get_cookie():
    return request.cookies.get("capybara", "")


@app.route("/get_header")
def get_header():
    return request.headers.get("Foo", "")


@app.route("/get_header_via_redirect")
def get_header_via_redirect():
    return flask.redirect("/get_header")


@app.route("/error")
def error():
    raise AppError()


@app.route("/import_error")
def import_error():
    raise ImportError("Simulated ImportError")


@app.route("/with_html")
def with_html():
    return render_template("with_html.html")


@app.route("/with_simple_html")
def with_simple_html():
    return render_template("with_simple_html.html")


@app.route("/<name>")
def view(name):
    return render_template("{}.html".format(name))


@app.route("/upload_empty", methods=["POST"])
def upload_empty():
    f = request.files.get("form[file]")

    if not f:
        return "Successfully ignored empty file field."
    else:
        return "Something went wrong."


@app.route("/upload", methods=["POST"])
def upload():
    document = request.files.get("form[document]")

    if document and document.filename:
        buf = []
        buf.append("Content-type: {0}".format(document.mimetype))
        buf.append("File content: {0}".format(document.read()))
        return " | ".join(buf)
    else:
        return "No file uploaded"


@app.route("/upload_multiple", methods=["POST"])
def upload_multiple():
    documents = request.files.getlist("form[multiple_documents][]")
    documents = [doc for doc in documents if doc.filename]

    if len(documents):
        buf = [str(len(documents))]

        for document in documents:
            buf.append("Content-type: {0}".format(document.mimetype))
            buf.append("File content: {0}".format(document.read()))

        return " | ".join(buf)
    else:
        return "No files uploaded"


if __name__ == "__main__":
    app.run()
