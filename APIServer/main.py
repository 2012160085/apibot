from zipgapbot import apiparser,configmaker,dbwork


try:
    work_conf = (configmaker.readconf("workconf.json"))
    lawd_codes = (configmaker.readconf("lawd_cd.json"))
except Exception as e:
    print(e)