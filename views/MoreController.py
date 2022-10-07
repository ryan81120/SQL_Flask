from flask import render_template, request
from flask import Blueprint
from Model import Home_DAL
import json


# Blueprint參數
Maps = Blueprint('Maps', __name__, url_prefix='/Maps', template_folder='templates')


@Maps.route("/")
def Google_Maps():
    return render_template("Maps.html")


# region RESTful API

@Maps.route("/", methods=["POST"])
def Home_maps_locations():
    print("Home_maps_locations")
    lst = []
    area = request.args.get('area')
    AreaId = Home_DAL.GET_AreaId_By_Area_Name(area)
    Hospital_Informations = Home_DAL.Get_Hospital_Informations_By_Area(str(AreaId.Id))
    for i in Hospital_Informations:
        dict_hospital = {'lat': "", 'lng': ""}
        dict_hospital["lat"] = i.Latitude
        dict_hospital["lng"] = i.Longitude
        lst.append(dict_hospital)
    return json.dumps(lst, ensure_ascii=False)

# endregion
