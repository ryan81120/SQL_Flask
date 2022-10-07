import time

from flask import Flask, render_template, redirect, request, jsonify
from flask import Blueprint
from Model import Home_DAL, Utility
from MialServer import MailServer
import json

# Blueprint參數
Home = Blueprint('Home', __name__, url_prefix='/Home', template_folder='templates')


# region Route

@Home.route('/')
def Home_Index():
    select_area = Home_DAL.GET_Areas()
    select_area.insert(0, {"AreaName": "全部"})
    Hospital_Informations = Home_DAL.Get_Hospital_Informations()
    print('進入Home_Index')
    return render_template("Index.html", Hospital_Informations=Hospital_Informations,
                           select_area=select_area, areaid="")


@Home.route('/Search')
def Home_Index_By_Area():
    select_area = Home_DAL.GET_Areas()
    select_area.insert(0, {"AreaName": "全部"})
    areaid = request.args.get('areaid')
    townshipid = request.args.get('townshipid')
    select_township = Home_DAL.GET_Township_By_Area_Id(areaid)
    select_township.insert(0, {"TownshipName": "全部"})

    if areaid == "":
        return redirect("/Home")
    if townshipid != "":
        townshipname = Home_DAL.GET_Township_By_Township_Id(townshipid)
        sql_like = f'%{townshipname.TownshipName}%'
        Hospital_Informations = Home_DAL.Get_Hospital_Informations_By_Area(areaid, sql_like)

    if townshipid == "":
        townshipid = 0
        Hospital_Informations = Home_DAL.Get_Hospital_Informations_By_Area(areaid)

    print('進入Home_Index_以搜尋完地區')
    return render_template("Index.html", Hospital_Informations=Hospital_Informations, select_area=select_area,
                           select_township=select_township, areaid=int(areaid), townshipid=int(townshipid))


@Home.route('/Edit', methods=["POST"])
def Home_Edit():
    HospitalId = request.form.get('HospitalId')
    Hospital_Information = Home_DAL.Get_Hospital_Information_By_Id(HospitalId)
    print('Home_Edit')
    return render_template("Edit.html", Hospital_Information=Hospital_Information)


@Home.route('/Add')
def Home_Add():
    return render_template("Add.html")


@Home.route("/Map")
def Home_map():
    return render_template("Map.html")


@Home.route("/Server")
def Home_Server():
    return render_template("opinion.html")


# endregion Route

# region RESTful API

@Home.route('/Edit', methods=["PUT"])
def Home_Edit_Update():
    data = json.loads(request.get_data())
    print('Home_Edit_Update')
    data_vaule = [data["hospitalname"], data["hospitaladdress"]]
    if '' in data_vaule:
        msg = {'code': 4, 'msg': "編輯失敗，請填寫完整資料", 'title': "失敗"}
        return json.dumps(msg, ensure_ascii=False)

    Areas = Home_DAL.GET_Areas()
    # 檢查 地區是否存在做id mapping
    data = Utility.re_arae(data, Areas)
    if data["area_id"] > max(Areas)[0]:
        Home_DAL.INSERT_Area(data["area_name"])

    # 檢查 行政區是否存在做id mapping
    Townships = Home_DAL.GET_Township_By_Area_Id(data["area_id"])
    has_township, township_name = Utility.re_township(data, Townships)
    print(has_township, township_name)
    if not has_township:
        Home_DAL.INSERT_Township(township_name, data["area_id"])

    if Home_DAL.UPDATE_Hospital_Information(data):
        msg = {'code': 1, 'msg': "編輯成功", 'title': "成功"}
    else:
        msg = {'code': 4, 'msg': "編輯失敗，請聯絡管理系統管理員", 'title': "失敗"}
    return json.dumps(msg, ensure_ascii=False)


@Home.route('/Add', methods=["POST"])
def Home_Add_DAL():
    data = json.loads(request.get_data())
    print('Home_Add_DAL')
    data_vaule = [data["hospitalname"], data["hospitaladdress"]]
    if '' in data_vaule:
        msg = {'code': 4, 'msg': "新增失敗，請填寫完整資料", 'title': "失敗"}
        return json.dumps(msg, ensure_ascii=False)
    Areas = Home_DAL.GET_Areas()
    #檢查 地區是否存在做id mapping
    data = Utility.re_arae(data, Areas)
    if data["area_id"] > max(Areas)[0]:
        Home_DAL.INSERT_Area(data["area_name"])

    # 檢查 行政區是否存在做id mapping
    Townships = Home_DAL.GET_Township_By_Area_Id(data["area_id"])
    has_township, township_name = Utility.re_township(data, Townships)
    print(has_township, township_name)
    if not has_township:
        Home_DAL.INSERT_Township(township_name, data["area_id"])

    # 檢查是否此醫院以在資料庫
    if Home_DAL.Get_Hospital_Information_By_Name(data["hospitalname"]) is not None:
        msg = {'code': 4, 'msg': "新增失敗，此醫院名稱已存在", 'title': "失敗"}
        return json.dumps(msg, ensure_ascii=False)
    if Home_DAL.INSERT_Hospital_Information(data):
        msg = {'code': 1, 'msg': "新增成功", 'title': "成功"}
    else:
        msg = {'code': 4, 'msg': "新增失敗，請聯絡管理系統管理員", 'title': "失敗"}
    return json.dumps(msg, ensure_ascii=False)


@Home.route('/Del', methods=["DELETE"])
def Home_Del_DAL():
    data = json.loads(request.get_data())
    print('Home_Del_DAL')
    if Home_DAL.DELETE_Hospital_Information(data['id']):
        msg = {'code': 1, 'msg': "刪除成功", 'title': "成功"}
    else:
        msg = {'code': 4, 'msg': "刪除失敗，請聯絡管理系統管理員", 'title': "失敗"}
    return json.dumps(msg, ensure_ascii=False)


@Home.route("/Server", methods=["POST"])
def Home_Server_sendmail():
    data = json.loads(request.get_data())
    print('Home_Server_sendmail')
    if "" in data.values():
        return json.dumps({'code': 4, 'msg': "表格請填寫完整", 'title': "失敗"}, ensure_ascii=False)

    # region 寄信流程
    if Home_DAL.INSERT_Mail(data):
        msg = {'code': 1, 'msg': "感謝收到您寶貴的意見~", 'title': "成功"}
        if MailServer.send_mail(data["problem"], data["statement"], data["email"]):
            Home_DAL.UPDATE_Success_Mail()
    else:
        msg = {'code': 4, 'msg': "信件發送失敗，請聯絡管理系統管理員", 'title': "失敗"}
    return json.dumps(msg, ensure_ascii=False)
    # endregion


@Home.route("/GetTownship", methods=["POST"])
def GetTownship():
    data = json.loads(request.get_data())
    row_data = []
    select_township = Home_DAL.GET_Township_By_Area_Id(data['areaid'])
    for i in select_township:
        msg = {'Id': "", 'TownshipName': ""}
        msg['Id'] = i.Id
        msg['TownshipName'] = i.TownshipName
        row_data.append(msg)
    row_data.insert(0, {'Id': "", "TownshipName": "全部"})
    return jsonify(row_data)


# endregion RESTful API
