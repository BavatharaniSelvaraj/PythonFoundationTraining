import mysql.connector
from util.DBPropertyUtil import DBPropertyUtil

def getConnection():
    props = DBPropertyUtil.getPropertyString('util/db.properties')
    return mysql.connector.connect(
        host=props['host'],
        user=props['username'],
        password=props['password'],
        database=props['database'],
        port=int(props['port'])
    )