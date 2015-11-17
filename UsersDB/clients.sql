DROP DATABASE IF EXISTS clients;
CREATE DATABASE clients;
USE clients;

DROP TABLE IF EXISTS client_profile;
CREATE TABLE client_profile (
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(255),
    pass CHAR(40),
	email VARCHAR(255),
	phone VARCHAR(15),
	language VARCHAR(2) DEFAULT 'en',
	store_location VARCHAR(1) DEFAULT '1',
	notifications_alert VARCHAR(1) DEFAULT '1',
	recommendations_alert VARCHAR(1) DEFAULT '1',
    theme VARCHAR(1) DEFAULT '1',
	registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    google_registraton_token VARCHAR(255),
	PRIMARY KEY (id)
);

DELIMITER $$
DROP FUNCTION IF EXISTS client_sign_up;
CREATE FUNCTION client_sign_up (
	in_username VARCHAR(255),
	in_pass CHAR(40),
	in_email VARCHAR(255),
	in_phone VARCHAR(15),
    in_google_registraton_token VARCHAR(255)
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

	IF EXISTS (
		SELECT username
		FROM client_profile
		WHERE username = in_username
	)
	THEN
		RETURN '01';
	ELSEIF EXISTS (
		SELECT email
		FROM client_profile
		WHERE email = in_email
	)
	THEN
		RETURN '02';
	ELSEIF EXISTS (
		SELECT phone
		FROM client_profile
		WHERE phone = in_phone
	)
	THEN
		RETURN '03';
	ELSE
		INSERT INTO client_profile (username, pass, email, phone, google_registraton_token)
        VALUES (in_username, in_pass, in_email, in_phone, in_google_registraton_token);

        GET DIAGNOSTICS rows = ROW_COUNT;

        IF code = '00000' AND rows = 1 THEN
            RETURN CONCAT('1', '|', (SELECT LAST_INSERT_ID()));
        ELSE
            RETURN '0';
        END IF;
	END IF;
END $$

DROP FUNCTION IF EXISTS client_sign_in;
CREATE FUNCTION client_sign_in (
	in_username VARCHAR(255),
	in_pass CHAR(40),
    in_google_registraton_token VARCHAR(255)
)
RETURNS TEXT
BEGIN
	DECLARE ret_id INT;
	DECLARE ret_email VARCHAR(255);
	DECLARE ret_phone VARCHAR(15);
	DECLARE ret_language VARCHAR(2);
	DECLARE ret_store_location VARCHAR(1);
	DECLARE ret_notifications_alert VARCHAR(1);
	DECLARE ret_recommendations_alert VARCHAR(1);
    DECLARE ret_theme VARCHAR(1);

    DECLARE code CHAR(5) DEFAULT '00000';
    DECLARE rows INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            code = RETURNED_SQLSTATE;
    END;

	SELECT
		id, email, phone, language, store_location,
		notifications_alert, recommendations_alert, theme
	INTO
		ret_id, ret_email, ret_phone, ret_language, ret_store_location,
		ret_notifications_alert, ret_recommendations_alert, ret_theme
	FROM client_profile
	WHERE username = in_username AND pass = in_pass;

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows = 1 THEN
        UPDATE client_profile
        SET google_registraton_token = in_google_registraton_token
        WHERE id = ret_id;

        RETURN CONCAT(
            '1', '|', ret_id, '|', ret_email, '|', ret_phone, '|', ret_language, '|',
            ret_store_location, '|', ret_notifications_alert, '|',
            ret_recommendations_alert, '|', ret_theme
        );
    ELSE
        RETURN '0';
    END IF;
END $$

DROP FUNCTION IF EXISTS google_sign_in;
CREATE FUNCTION google_sign_in (
	in_email VARCHAR(255)
)
RETURNS TEXT
BEGIN
    DECLARE ret_id INT;
    DECLARE ret_username VARCHAR(255);
    DECLARE temp_pass CHAR(40);
    DECLARE ret_pass VARCHAR(1);
    DECLARE ret_phone VARCHAR(15);
    DECLARE ret_language VARCHAR(2);
    DECLARE ret_store_location VARCHAR(1);
    DECLARE ret_notifications_alert VARCHAR(1);
    DECLARE ret_recommendations_alert VARCHAR(1);
    DECLARE ret_theme VARCHAR(1);

    DECLARE code CHAR(5) DEFAULT '00000';
    DECLARE rows INT;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            code = RETURNED_SQLSTATE;
    END;

	IF EXISTS (
		SELECT email
		FROM client_profile
		WHERE email = in_email
	)
	THEN
        SELECT
            id, username, pass, phone, language, store_location,
            notifications_alert, recommendations_alert, theme
        INTO
            ret_id, ret_username, temp_pass, ret_phone, ret_language, ret_store_location,
            ret_notifications_alert, ret_recommendations_alert, ret_theme
        FROM client_profile
        WHERE email = in_email;

        IF temp_pass = '' THEN
            SET ret_pass = '0';
        ELSE
            SET ret_pass = '1';
        END IF;

        GET DIAGNOSTICS rows = ROW_COUNT;

        IF code = '00000' AND rows = 1 THEN
            RETURN CONCAT(
                '1', '|', ret_id, '|', ret_username, '|', ret_pass, '|', ret_phone, '|', ret_language, '|',
                ret_store_location, '|', ret_notifications_alert, '|',
                ret_recommendations_alert, '|', ret_theme
            );
        ELSE
            RETURN '0';
        END IF;
	ELSE
		RETURN google_sign_up(in_email);
	END IF;
END $$

DROP FUNCTION IF EXISTS google_sign_up;
CREATE FUNCTION google_sign_up (
	in_email VARCHAR(255)
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

	INSERT INTO client_profile (username, pass, email, phone)
    VALUES ('', '', in_email, '');

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows = 1 THEN
	   RETURN CONCAT('2', '|', (SELECT LAST_INSERT_ID()));
    ELSE
        RETURN '0';
    END IF;
END $$

DROP FUNCTION IF EXISTS client_profile_update;
CREATE FUNCTION client_profile_update (
    in_id INT,
	in_username VARCHAR(255),
	in_email VARCHAR(255),
	in_phone VARCHAR(15)
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

    IF EXISTS (
		SELECT username
		FROM client_profile
		WHERE username = in_username AND id <> in_id
	)
	THEN
		RETURN '01';
	ELSEIF EXISTS (
		SELECT email
		FROM client_profile
		WHERE email = in_email AND id <> in_id
	)
	THEN
		RETURN '02';
	ELSEIF EXISTS (
		SELECT phone
		FROM client_profile
		WHERE phone = in_phone AND id <> in_id
	)
	THEN
		RETURN '03';
	ELSE
        UPDATE client_profile
        SET username = in_username,
            email = in_email,
            phone = in_phone
        WHERE id = in_id;
        GET DIAGNOSTICS rows = ROW_COUNT;

        IF code = '00000' AND rows > 0 THEN
            RETURN '1';
        ELSE
            RETURN '0';
        END IF;
	END IF;
END $$

DROP FUNCTION IF EXISTS client_settings_update;
CREATE FUNCTION client_settings_update (
    in_id INT,
    in_language VARCHAR(2),
	in_store_location VARCHAR(1),
	in_notifications_alert VARCHAR(1),
	in_recommendations_alert VARCHAR(1),
    in_theme VARCHAR(1)
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

    UPDATE client_profile
    SET language = in_language,
        store_location = in_store_location,
        notifications_alert = in_notifications_alert,
        recommendations_alert = in_recommendations_alert,
        theme = in_theme
    WHERE id = in_id;

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows > 0 THEN
        RETURN '1';
    ELSE
        RETURN '0';
    END IF;
END $$

DROP FUNCTION IF EXISTS client_existing_password_update;
CREATE FUNCTION client_existing_password_update (
    in_id INT,
    in_old_pass CHAR(40),
    in_new_pass CHAR(40)
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

    UPDATE client_profile
    SET pass = in_new_pass
    WHERE id = in_id AND pass = in_old_pass;

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows > 0 THEN
        RETURN '1';
    ELSE
        RETURN '0';
    END IF;
END $$

DROP FUNCTION IF EXISTS client_forgotten_password_reset;
CREATE FUNCTION client_forgotten_password_reset (
    in_email VARCHAR(255),
    in_new_pass CHAR(40)
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

    UPDATE client_profile
    SET pass = in_new_pass
    WHERE email = in_email;

    GET DIAGNOSTICS rows = ROW_COUNT;

    IF code = '00000' AND rows > 0 THEN
        RETURN '1';
    ELSE
        RETURN '0';
    END IF;
END $$

-- ------------------------------------------------ DEBUGGING CODE ----------------------------------------------------

-- SELECT client_sign_up('u1', 'p1', 'e1', 'ph1');
-- SELECT client_existing_password_update(1, 'p1', 'p');
-- SELECT client_existing_password_update(1, 'p1', 'p2');
-- SELECT client_existing_password_update(2, 'p1', 'p3');
-- SELECT client_forgotten_password_reset('e1', 'p10');
-- SELECT client_forgotten_password_reset('e', 'p100');
--
-- SELECT google_sign_in('e8');
-- SELECT google_new_password_register(1, 'p30');
-- SELECT google_new_password_register(2, 'p30');
-- SELECT client_profile_update(2, 'u10', 'e8', 'ph0');
-- SELECT google_new_password_register(2, 'p30');
-- SELECT client_sign_up('u2', 'p2', 'e2', 'ph2');
-- SELECT client_profile_update(1, 'u1', e', 'ph');
-- SELECT client_profile_update(1, 'u', 'e', 'ph');
-- SELECT client_settings_update(1, 'en', '2', '1', '1', '1');
-- SELECT client_profile_update(3, 'u10', 'p10', 'e0', 'ph0');
-- SELECT client_sign_up('', '', 'e', '');
-- SELECT client_sign_up('u1', 'p1', 'e1', 'ph1');
-- SELECT client_sign_up('u', 'p1', 'e1', 'ph1');
-- SELECT client_sign_up('u', 'p1', 'e', 'ph1');
-- SELECT client_sign_up('u2', 'p2', 'e2', 'ph2');
-- SELECT client_sign_in('u1', 'p1');
-- SELECT client_sign_in('u', 'p');
-- SELECT client_sign_in('', '');
-- SELECT google_sign_in('e1');
-- SELECT google_sign_in('e2');
-- SELECT google_sign_in('e1');
-- SELECT google_sign_in('e2');

-- --------------------------------------------------------------------------------------------------------------------
