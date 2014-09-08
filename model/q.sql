--select u.*, STRING_AGG(distinct p.name, ',') as permissions_name, STRING_AGG(distinct c.name, ',') as cellars_name from "User" u left join "Permission" p on p.id = any(u.permissions) left join "Cellar" c on c.id = any(u.cellar_permissions) group by u.id limit 1
--select * from "Cellar" limit 100 offset 0
--select * from "Permission"
--select * from "Kardex"
update "User" set cellar_permissions = cellar_permissions - array[1]