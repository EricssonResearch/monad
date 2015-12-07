DROP DATABASE IF EXISTS vehicles;
CREATE DATABASE vehicles;
USE vehicles;

-- DROP TABLE IF EXISTS vehicle_profile;
CREATE TABLE vehicle_profile (
    vehicle_id INT NOT NULL AUTO_INCREMENT,
    driver_id VARCHAR(255),
    pass CHAR(40),
    bus_line VARCHAR(10),
    google_registration_token VARCHAR(255),
    PRIMARY KEY (vehicle_id)
);

DELIMITER $$
-- DROP FUNCTION IF EXISTS vehicle_sign_up;
CREATE FUNCTION vehicle_sign_up (
    in_driver_id VARCHAR(255),
    in_pass CHAR(40),
    in_bus_line VARCHAR(10)
)
RETURNS TEXT
BEGIN
    DECLARE code CHAR(5) DEFAULT '00000';
    DECLARE rows INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            code = RETURNED_SQLSTATE;
    END;

    INSERT INTO vehicle_profile (driver_id, pass, bus_line, google_registration_token)
    VALUES (in_driver_id, SHA1(MD5(in_pass)), in_bus_line, '');

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows > 0 THEN
        RETURN '1';
    ELSE
        RETURN '0';
    END IF;
END $$

-- DROP FUNCTION IF EXISTS vehicle_sign_in;
CREATE FUNCTION vehicle_sign_in (
    in_driver_id VARCHAR(255),
    in_pass CHAR(40),
    in_bus_line VARCHAR(10)
)
RETURNS TEXT
BEGIN
    DECLARE ret_vehicle_id INT;

    DECLARE code CHAR(5) DEFAULT '00000';
    DECLARE rows INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            code = RETURNED_SQLSTATE;
    END;

    SELECT vehicle_id INTO ret_vehicle_id
    FROM vehicle_profile
    WHERE driver_id = in_driver_id AND pass = in_pass AND bus_line = in_bus_line;

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows > 0 THEN
        RETURN CONCAT('1', '|', ret_vehicle_id);
    ELSE
        RETURN '0';
    END IF;
END $$

-- DROP FUNCTION IF EXISTS get_google_registration_token;
CREATE FUNCTION get_google_registration_token (
    in_vehicle_id INT
)
RETURNS VARCHAR(255)
BEGIN
    DECLARE ret_google_registration_token VARCHAR(255);
    DECLARE code CHAR(5) DEFAULT '00000';
    DECLARE rows INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            code = RETURNED_SQLSTATE;
    END;

    SELECT google_registration_token
    INTO ret_google_registration_token
    FROM vehicle_profile
    WHERE vehicle_id = in_vehicle_id;

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows > 0 THEN
        RETURN ret_google_registration_token;
    ELSE
        RETURN '';
    END IF;
END $$

-- DROP FUNCTION IF EXISTS set_google_registration_token;
CREATE FUNCTION set_google_registration_token (
    in_vehicle_id INT,
    in_google_registration_token VARCHAR(255)
)
RETURNS TEXT
BEGIN
    DECLARE code CHAR(5) DEFAULT '00000';
    DECLARE rows INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            code = RETURNED_SQLSTATE;
    END;

    UPDATE vehicle_profile
    SET google_registration_token = in_google_registration_token
    WHERE vehicle_id = in_vehicle_id;

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows > 0 THEN
        RETURN '1';
    ELSE
        RETURN '0';
    END IF;
END $$

DELIMITER ;

-- ------------------------------------------------- DEBUGGING CODE ---------------------------------------------------

SELECT vehicle_sign_up('d1', 'p1', '1');

-- --------------------------------------------------------------------------------------------------------------------
