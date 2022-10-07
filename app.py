from flask import Flask, render_template, redirect, url_for
from views.HomeController import Home as blueprint_Home
from views.MoreController import Maps as blueprint_Maps
from views.NewController import News as blueprint_News
from flask_caching import Cache


app = Flask(__name__, static_url_path='/static')
app.register_blueprint(blueprint_Home)
app.register_blueprint(blueprint_Maps)
app.register_blueprint(blueprint_News)

# region 可以對全部app route設定Cache 共同參數
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 50})
# app.config.from_mapping(config)
# cache = Cache(app)
# endregion


# region route初始化
# @cache.cached(timeout=50)
@app.route("/")
def hello():
    return redirect(url_for('Home.Home_Index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('Page_not_found.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('Page_not_found.html'), 500

# endregion route初始化


if __name__ == '__main__':
    app.run()

