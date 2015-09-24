DROP SCHEMA IF EXISTS `MONAD`;

CREATE SCHEMA `MONAD`;

USE `MONAD`;

CREATE TABLE USER_PROFILE(
	username varchar(255) NOT NULL,
	firstname varchar(255) NOT NULL,
	lastname varchar(255) NOT NULL,
	email varchar(255) UNIQUE,
	phone varchar(15) UNIQUE NOT NULL,
	pass char(40) NOT NULL,						-- ??
	-- role tinyint(1) unsigned NOT NULL DEFAULT '0',
	-- birthday DATE,
	registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	-- days_of_inactivity int DEFAULT 0,
	activated tinyint(1) unsigned NOT NULL DEFAULT '0',
	PRIMARY KEY (username)
);


CREATE TABLE VEHICLE(
	ID int NOT NULL AUTO_INCREMENT,
	licence varchar(15) UNIQUE NOT NULL,
	current_driver varchar(255),
	PRIMARY KEY(ID)
);

CREATE TABLE DRIVER(
	username varchar(255) NOT NULL,
	pass char(40),
	PRIMARY KEY(username)
);

ALTER TABLE VEHICLE AUTO_INCREMENT = 100;
ALTER TABLE VEHICLE ADD FOREIGN KEY(current_driver) REFERENCES DRIVER(username);

-- pass (password) field depends on the hashing algorithm. e.g. here is SHA-1
-- role is either 0 for a simple user/passenger or '1' for driver. we presume that
-- the default is a user/passenger otherwise we have to explicitly change it

-- same with the activated field where the default is '0' (not activated) and as soon
-- as the user activates his/her account it is updated to '1'

DELIMITER $$

CREATE FUNCTION `SIGNUP` (uname VARCHAR(255),fname VARCHAR(255), lname VARCHAR(255), em VARCHAR(255),  ph VARCHAR(15), pass VARCHAR(255))
RETURNS INTEGER
BEGIN
	IF EXISTS(SELECT * FROM USER_PROFILE WHERE username = uname)
	THEN
		RETURN 0;
	ELSEIF EXISTS (SELECT * FROM USER_PROFILE WHERE email = em)
	THEN
		RETURN 1;
	ELSEIF EXISTS (SELECT * FROM USER_PROFILE WHERE phone = ph)
	THEN
		RETURN 2;
	ELSE
		INSERT INTO USER_PROFILE (username, firstname, lastname, email, phone, pass) VALUES (uname, fname, lname, em, ph, sha1(pass));
		RETURN 3;
	END IF;
END $$

-- DELIMITER $$

CREATE FUNCTION `SIGNIN` (uname VARCHAR(255), pass VARCHAR(255))
RETURNS bit
BEGIN
	IF EXISTS(SELECT * FROM USER_PROFILE WHERE username = uname AND sha1(pass) = pass)
	THEN
		RETURN 1;
	ELSE
		RETURN 0;
	END IF;
END $$

DELIMITER ;

-- creating the first driver
/*
INSERT INTO USER_PROFILE(username, firstname, lastname, email, phone, pass)
VALUES('chge','Charalampos', 'Georgiadis', 'babispasg@gmail.com', '1234567890', 'mypass');

INSERT INTO USER_PROFILE(username, firstname, lastname, email, phone, pass)
VALUES('chko', 'Charalampos', 'Kominos', 'charis@gmail.com', '0987654321', '1234');

INSERT INTO DRIVER(username) VALUES ('driver1');

INSERT INTO VEHICLE(licence, current_driver) VALUES ('1324756890', 'driver1');

SELECT SIGNUP('cGge','Charalampos', 'Georgiadis', 'babispas@gmail.com', '1234567891', 'mypassword');
SELECT SIGNIN('chge','mypass');
*/

-- SELECT COUNT(*) FROM USER_PROFILE WHERE firstname = 'Ciera';
-- SELECT * FROM VEHICLE;


-- NOTES!! activated OR NON activated USERS
