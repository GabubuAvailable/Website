from flask import Flask, render_template, request, abort
from werkzeug.urls import url_encode
import config

import osc

OpenShopChannel = osc.API()
OpenShopChannel.load_packages()

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def home():
    return render_template('pages/home.html')


@app.route("/publish")
def publish():
    return render_template('pages/publish.html', packages=OpenShopChannel.get_packages())


@app.route("/feedback")
def feedback():
    return render_template('pages/feedback.html')


@app.route("/about")
def about():
    return render_template('pages/about.html')


@app.route("/beta")
def beta():
    return render_template('pages/beta.html')


@app.route("/library")
def apps():
    # handle pagination
    items_per_page = 10
    if request.args.get("p"):
        page = int(request.args.get("p"))
    else:
        page = 1
    end_index = page * items_per_page
    start_index = end_index - items_per_page
    packages = OpenShopChannel.get_packages(developer=request.args.get("coder"))

    return render_template('pages/library.html', packages=packages[start_index:end_index], page=page)


@app.route("/library/app/<name>")
def application(name):
    # error handling in case the app doesn't exist
    try:
        category = OpenShopChannel.package_by_name(name)["category"]
    except Exception:
        abort(404)
    return render_template('pages/app.html', package=OpenShopChannel.package_by_name(name), packages=OpenShopChannel.get_packages())


@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html')


if __name__ == '__main__':
    app.run(port=config.port)
