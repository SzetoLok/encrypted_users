Create database if not exists gekko_users;
use gekko_users;
drop table CLIENT1; 

CREATE TABLE `CLIENT1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
 --  `last_login` datetime(6) DEFAULT NULL,
  `username` varchar(64) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(16) DEFAULT NULL,
 --  `email_verified` tinyint(1) NOT NULL,
--   `terms_agreed` tinyint(1) NOT NULL,
--   `register_time` datetime(6) NOT NULL,
--   `is_valid` tinyint(1) NOT NULL,
--   `is_locked` tinyint(1) NOT NULL,
--   `option` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;

Insert into `CLIENT1` (id, password, username, email, phone_number)Values(1,'123','lucas','lucas@abc', '1');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(2,'123','sam','sam@abc', '2');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(3,'123','tom','tom@abc', '3');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(4,'123','john','john@ab', '4');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(5,'123','mary','mary@ab', '5');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(6,'123','lebron','lebron@abc', '6');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(7,'123','kobe','kobe@abc', '7');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(8,'123','carmelo','carmelo@abc', '8');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(9,'123','stephen','stehphen@ab', '9');
Insert into `CLIENT1` (id, password, username, email, phone_number)Values(10,'123','jordan','jordan@old', '10')

