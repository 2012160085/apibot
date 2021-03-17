import json
import os
def readconf(filename):
    if checkexist(filename):
        with open(filename,encoding='utf-8') as json_file:
            conf_data = json.load(json_file)
        return conf_data
    else:
        raise Exception("설정파일이 존재하지 않음")

def checkexist(filename):
    return os.path.isfile(filename) 