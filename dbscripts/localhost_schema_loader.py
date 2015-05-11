from lp.tools.scriptloader import ScriptLoader

sl = ScriptLoader()
sl.dbname = "sites"
sl.user = "postgres"
sl.host = "localhost"
sl.password = "12345"
sl.script_file = "schema.sql"


sl.delete_old()
sl.execute()
