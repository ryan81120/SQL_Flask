from flask import render_template, request
from flask import Blueprint
from Model import News_DAL
from crawler_server import crawler_Health_Fukube_News
import json


# Blueprint參數
News = Blueprint('News', __name__, url_prefix='/News', template_folder='templates')


@News.route("/")
def News_Index():
    News_Informations = News_DAL.Get_News_Informations()
    return render_template("News.html", News_Informations=News_Informations)


@News.route("/Update", methods=["POST"])
def News_Update():
    if crawler_Health_Fukube_News.crawler_news():
        msg = {'code': 1, 'msg': "更新成功", 'title': "成功"}
    else:
        msg = {'code': 4, 'msg': "更新失敗，請聯絡管理系統管理員", 'title': "失敗"}
    return json.dumps(msg, ensure_ascii=False)
