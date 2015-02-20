from lp.tools.scriptloader import ScriptLoader

sl = ScriptLoader()
sl.dbname = "giani"
sl.user = "yichun"
sl.host = "localhost"  # solo se puede ejecutar directamente en el servidor
sl.password = "chachun88"

sl.delete_old()


# load this database backup with given configurations
sl.script_file = "back20150220.sql"  # last backup
sl.execute()
