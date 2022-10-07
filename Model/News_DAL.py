import pyodbc as pyodbc
from Model import config

# region SQL連線
sqlConn = pyodbc.connect(config.db_connect, autocommit=True)
cursor = sqlConn.cursor()


# endregion

# region 取得資料

def Get_News_Informations():
    """
    取得全部新聞資料
    :return: List
    """
    cursor.execute("""SELECT
       row_number() OVER (order by [Post_Date] DESC ) AS RowId
      ,[Id]
      ,[Title]
      ,[Url]
      ,[Post_Date]
      ,[Logtime]
  FROM [Hospital].[dbo].[Health_Fukube_News]""")
    return cursor.fetchall()


# endregion

