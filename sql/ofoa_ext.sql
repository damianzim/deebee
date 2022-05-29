  CREATE OR REPLACE FUNCTION "OFOA_AUTH" (p_email IN VARCHAR2, p_password IN RAW)
RETURN VARCHAR2
AS
    accounts NUMBER(1) := 0;
BEGIN
    SELECT COUNT(*) INTO accounts
    FROM clients
    WHERE email = p_email AND password = p_password;
    IF accounts > 0 THEN
        RETURN 'client';
    END IF;

    SELECT COUNT(*) INTO accounts
    FROM restaurants
    WHERE email = p_email AND password = p_password;
    IF accounts > 0 THEN
        RETURN 'restaurant';
    ELSE
        RETURN NULL;
    END IF;
END ofoa_auth;
