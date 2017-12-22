/*
MySQL version 5.5.58
author:KAI
SQL相关语句*/
SHOW DATABASES;--查看已有数据库
CREATE DATABASE system_key;--建立数据库

use system_key;
show tables;--查看当前数据库中所有数据表

source path_name/fc_project_tags.sql;--导入大型sql文件


rename TABLE fc_project_tags to sys_keywords;--重命名

DESC sys_keywords;--表的详情

/*
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| project_id | int(11)     | NO   | PRI | 0       |       |
| tag_name   | varchar(50) | NO   | PRI | 0       |       |
+------------+-------------+------+-----+---------+-------+

Since then, the required database is set.
*/