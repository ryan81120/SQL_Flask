import pyodbc as pyodbc
from Model import config

# region SQL連線
sqlConn = pyodbc.connect(config.db_connect, autocommit=True)
cursor = sqlConn.cursor()


# endregion

# region 取得資料

def Get_Hospital_Informations():
    """
    取得全部醫院資料
    :return: List
    """
    cursor.execute("""SELECT [Id]
        ,HI.[HospitalName]
        ,[HospitalAddress]
        ,[Telephone]
        ,[Longitude]
        ,[Latitude]
        ,[URL]
    FROM [Hospital].[dbo].[Hospital_Information] AS HI
    left join Hospital_Latitude_and_longitude AS HL
    ON HI.HospitalName = HL.HospitalName AND HI.Id = HL.Hospital_Information_Id""")
    return cursor.fetchall()


def Get_Hospital_Information_By_Id(Id):
    """
    取得單筆醫院資訊
    :param HospitalName: 醫院名稱
    :return: 一筆醫院名稱(List)
    """
    cursor.execute("""SELECT [Id]
      ,HI.[HospitalName]
      ,[HospitalAddress]
      ,[Telephone]
      ,[Longitude]
      ,[Latitude]
      ,[URL]
  FROM [Hospital].[dbo].[Hospital_Information] AS HI
  left join Hospital_Latitude_and_longitude AS HL
  ON HI.HospitalName = HL.HospitalName AND HI.Id = HL.Hospital_Information_Id
  WHERE Id= ?
  """, Id)
    return cursor.fetchone()


def Get_Hospital_Information_By_Name(Name):
    """
    取得單筆醫院資訊
    :param HospitalName: 醫院名稱
    :return: 一筆醫院名稱(List)
    """
    cursor.execute("""SELECT [Id]
      ,HI.[HospitalName]
      ,[HospitalAddress]
      ,[Telephone]
      ,[Longitude]
      ,[Latitude]
      ,[URL]
  FROM [Hospital].[dbo].[Hospital_Information] AS HI
  left join Hospital_Latitude_and_longitude AS HL
  ON HI.HospitalName = HL.HospitalName AND HI.Id = HL.Hospital_Information_Id
  WHERE HI.[HospitalName]= ?
  """, Name)
    return cursor.fetchone()


def Get_Hospital_Informations_By_Area(areaid, township='%%'):
    """
        取得地區醫院資料
    :param area: 地區
    :param township: 行政區 預設全部
    :return: list
    """
    print("DAL:" + areaid)

    cursor.execute("""SELECT [Id]
        ,HI.[HospitalName]
        ,[HospitalAddress]
        ,[Telephone]
        ,[Longitude]
        ,[Latitude]
        ,[URL]
    FROM [Hospital].[dbo].[Hospital_Information] AS HI
    left join Hospital_Latitude_and_longitude AS HL
    ON HI.HospitalName = HL.HospitalName AND HI.Id = HL.Hospital_Information_Id
    WHERE Area_Id= ? AND HospitalAddress LIKE ?""", areaid, township)
    return cursor.fetchall()


def GET_Areas():
    """
    取得全部縣市
    :return:
    """
    cursor.execute("""SELECT 
    [Id],
    AreaName,
    [Flag]
    FROM [Hospital].[dbo].[Area]
    WHERE Flag = 1""")
    return cursor.fetchall()


def GET_AreaId_By_Area_Name(name):
    """
    取得該縣市編號
    :return:
    """
    cursor.execute("""SELECT [Id]
      ,[AreaName]
      ,[Flag]
    FROM [Hospital].[dbo].[Area]
    WHERE AreaName= ?""", name)
    return cursor.fetchone()


def GET_Township_By_Area_Id(Id):
    """
    取得單縣市全部地區
    :return:
    """
    cursor.execute("""SELECT [Id]
      ,[TownshipName]
      ,[Area_Id]
      ,[Flag]
  FROM [Hospital].[dbo].[Township]
  WHERE Area_Id = ?""", Id)
    return cursor.fetchall()


def GET_Township_By_Township_Id(Id):
    """
    取得單縣市全部地區
    :return:
    """
    cursor.execute("""SELECT [Id]
      ,[TownshipName]
      ,[Area_Id]
      ,[Flag]
  FROM [Hospital].[dbo].[Township]
  WHERE Id = ?""", Id)
    return cursor.fetchone()

# endregion

# region 修改資料


def UPDATE_Hospital_Information(data):
    """
    更新醫院資訊
    :param data: 單筆醫院資訊(dict)
    :return: bool
    """
    try:
        cursor.execute("""UPDATE [Hospital_Information]
        SET
            HospitalName= ?,
            HospitalAddress= ?,
            Telephone= ?,
            Area_Id= ?,
            URL= ?
        WHERE Id = ?
      """, data['hospitalname'], data['hospitaladdress'], data['telephone'], data['area_id'], data['url'],
                       data['id'])
        cursor.execute("""UPDATE Hospital_Latitude_and_longitude
                        SET
                            HospitalName= ?,
                            Longitude= ?,
                            Latitude=?
                        WHERE Hospital_Information_Id= ?
                      """, data['hospitalname'], data['longitude'], data['latitude'], data['id'])
        flag = True
    except Exception as e:
        flag = False
        print(e)
    finally:
        return flag


def UPDATE_Success_Mail():
    """
    更新信件狀態
    :return: bool
    """
    try:
        cursor.execute("""UPDATE [Mail]
        SET
            Flag= 1, Logtime= GETDATE()d
         WHERE [Id] =(SELECT MAX(Id) FROM [Mail])""")
        flag = True
        print("郵件狀態更新完成")
    except Exception as e:
        flag = False
        print(e)
    finally:
        return flag


# endregion

# region 新增資料


def INSERT_Hospital_Information(data):
    """
    新增醫院資訊
    :param data: 單筆醫院資訊(dict)
    :return: bool
    """
    try:
        print(data)
        cursor.execute("""INSERT INTO
        Hospital_Information
        (HospitalName, HospitalAddress, Telephone, Area_Id, URL)
        VALUES(?, ?, ?, ?, ?)
      """, data['hospitalname'], data['hospitaladdress'], data['telephone'], data['area_id'], data['url'])
        cursor.execute("""INSERT INTO
                        Hospital_Latitude_and_longitude
                        (HospitalName, Longitude, Latitude)
                        VALUES(?, ?, ?)
                      """, data['hospitalname'], data['longitude'], data['latitude'])
        flag = True
    except Exception as e:
        flag = False
        print(e)
    finally:
        return flag


def INSERT_Area(areaname):
    """
    新增地區
    :param areaname: 地區名
    :return: bool
    """
    try:
        cursor.execute("""INSERT INTO
        [Area]
        (AreaName, Flag)
        VALUES(?, 1)""", areaname)
        flag = True
    except Exception as e:
        flag = False
        print(e)
    finally:
        return flag


def INSERT_Township(townshipname, areaid):
    """
    新增行政區
    :param townshipname: 行政區名
    :param areaid: 地區編號
    :return: bool
    """
    try:
        cursor.execute("""INSERT INTO
        [Township]
        (TownshipName, Area_Id, Flag)
        VALUES(?, ?, 1)""", townshipname, areaid)
        flag = True
    except Exception as e:
        flag = False
        print(e)
    finally:
        return flag


def INSERT_Mail(data):
    """
    新增郵件訊息
    :param data: 郵件訊息data(obj)
    :return: bool
    """
    try:
        print("準備新增郵件")
        cursor.execute("""INSERT INTO
        Mail
        (Usermail, Problem, Statement, Flag, Logtime)
        VALUES(?, ?, ?, 0, GETDATE())""", data["email"], data["problem"], data["statement"])
        flag = True
    except Exception as e:
        flag = False
        print(e)
    finally:
        return flag


# endregion

# region 刪除資料

def DELETE_Hospital_Information(id):
    """
    刪除醫院資訊
    :param id: 單筆醫院編號
    :return: bool
    """
    try:
        print("準備刪除")
        cursor.execute("""DELETE FROM Hospital_Latitude_and_longitude
                WHERE Hospital_Information_Id= ?""", id)
        cursor.execute("""DELETE FROM Hospital_Information
                        WHERE Id= ?""", id)
        flag = True
    except Exception as e:
        flag = False
        print(e)
    finally:
        return flag


# endregion

