/*
MySQL version 5.5.58
author:KAI
SQL������*/
SHOW DATABASES;--�鿴�������ݿ�
CREATE DATABASE system_key;--�������ݿ�

use system_key;
show tables;--�鿴��ǰ���ݿ����������ݱ�

source path_name/fc_project_tags.sql;--�������sql�ļ�


rename TABLE fc_project_tags to sys_keywords;--������

DESC sys_keywords;--�������

/*
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| project_id | int(11)     | NO   | PRI | 0       |       |
| tag_name   | varchar(50) | NO   | PRI | 0       |       |
+------------+-------------+------+-----+---------+-------+

Since then, the required database is set.
*/