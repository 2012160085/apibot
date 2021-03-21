import pymysql
from . import logger
#db

__configure__ = None
__connection__ = None

def setconfigure(conf):
    global __configure__
    __configure__ = conf
    for key in ["db_url" ,"db_usr","db_pwd","db_name"]:
        if key not in conf.keys():
            raise Exception(key+" key not exist in config")
    return __configure__

def conn():
    global __connection__
    conf = __configure__
    print(conf)
    if __connection__ == None:
        _conn = pymysql.connect(host=conf["db_url"], user=conf["db_usr"], 
                               password=conf["db_pwd"], db=conf["db_name"],
                               charset='utf8')
        __connection__ = _conn
    return __connection__

def makequery(tablename, data, columnMapper):
    sql = "insert into " + tablename +" ("
    for i,d in enumerate(data):
        sql += ("," if i > 0 else "") + columnMapper[tablename][d]
    sql += ") values ("
    for i,d in enumerate(data):
        sql += ("," if i > 0 else "") + "'" + ("" if data[d] == None else data[d])  + "'"
    sql += ")"
    return sql

def sel_pk(date,code):
    year = date[0:4]
    month = date[4:6]
    month = str(int(month))
    
    
    sql = "select concat(deal_year,'+',deal_month,'+',deal_day,'+',serial_number) from tb_api00 where deal_year = '" + year + "' and deal_month = '" + month + "' "
    sql += "and regional_code = '" + code + "'"
    cur = conn().cursor()
    cur.execute(sql)
    return set(map(lambda x : x[0], cur.fetchall()))

@logger.log_with_trycatch
def execute_commit(sql):
    conn().cursor().execute(sql)
    conn().commit()
