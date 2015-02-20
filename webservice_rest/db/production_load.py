from lp.tools.scriptloader import ScriptLoader

sl = ScriptLoader()
sl.dbname = "mprint"
sl.user = "mprint"
sl.host = "localhost"  # solo se puede ejecutar directamente en el servidor
sl.password = "mprint"

sl.delete_old()


# load this database backup with given configurations
sl.script_file = "back20150220.sql"  # last backup
sl.execute()
