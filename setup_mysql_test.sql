-- create database hbnb_dev_db, test database creation
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- add aa new user hbnb_dev with password 'hbnb_dev_pwd', user and password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- give privileges to hbnb_dev, acess rights
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
-- FLUSH PRIVILEGES;
