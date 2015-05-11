from lp.tools.scriptloader import ScriptLoader

sl = ScriptLoader()
sl.dbname = "sites"
sl.user = "ricardo"
sl.host = "ondev.today"
sl.password = "escuela16761"
sl.script_file = "schema.sql"


sl.delete_old()
sl.execute()
