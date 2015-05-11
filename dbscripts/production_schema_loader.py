from lp.tools.scriptloader import ScriptLoader

sl = ScriptLoader()
sl.dbname = "sites"
sl.user = "sites"
sl.host = "localhost"
sl.password = "loadingplay007"
sl.script_file = "schema.sql"


# sl.delete_old()
sl.execute()
