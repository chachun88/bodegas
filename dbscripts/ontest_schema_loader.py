from lp.tools.scriptloader import ScriptLoader
from config import *

sl = ScriptLoader()
sl.dbname = ONTEST_DB_NAME
sl.user = ONTEST_USER
sl.host = ONTEST_HOST
sl.password = ONTEST_PASSWORD
sl.script_file = "dbscripts/schema.sql"


sl.delete_old()
sl.execute()
