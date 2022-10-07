import re


def re_arae(data, areas):
    get_area = re.match(r'\S*[市,縣]{1}', data["hospitaladdress"])
    if get_area is not None:
        data["area_name"] = get_area[0]
        data["area_id"] = [i.Id for i in areas if i.AreaName == get_area[0]]
        if data["area_id"]:
            data["area_id"] = data["area_id"][0]
        else:
            data["area_id"] = max(areas)[0] + 1
    return data


def re_township(data, townships):
    get_area = re.match(r'\S*[市,縣]{1}', data["hospitaladdress"])
    address = data["hospitaladdress"].replace(get_area[0], "")
    get_township = re.match(r'\S*[區,鎮,鄉,市]{1}', address)
    if get_township is not None:
        township = get_township[0]
        has_township = [i.Id for i in townships if i.TownshipName == township]
        if has_township:
            return True, township
        else:
            return False, township

