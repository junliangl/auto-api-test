-- 给 mysql 创建 user
-- username: api_test  password: 123456

use mysql;
select host, user from user;
CREATE USER 'api_test'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'api_test'@'%' identified by '123456'  WITH GRANT OPTION;
flush privileges;
