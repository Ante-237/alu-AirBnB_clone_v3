-- create database hbnb_dev_db , name of databasse
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- add a new user hbnb_dev with password 'hbnb_dev_pwd' , user and password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- give privileges to hbnb_dev, access right grants
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
-- FLUSH PRIVILEGES;
