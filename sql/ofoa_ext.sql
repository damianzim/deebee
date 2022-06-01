  CREATE OR REPLACE FUNCTION "OFOA_AUTH" (p_email IN VARCHAR2, p_password IN RAW)
RETURN VARCHAR2
AS
    l_accounts NUMBER(1) := 0;
BEGIN
    SELECT COUNT(*) INTO l_accounts
    FROM clients
    WHERE email = p_email AND password = p_password;
    IF l_accounts > 0 THEN
      RETURN 'client';
    END IF;

    SELECT COUNT(*) INTO l_accounts
    FROM restaurants
    WHERE email = p_email AND password = p_password;
    IF l_accounts > 0 THEN
      RETURN 'restaurant';
    ELSE
      RETURN NULL;
    END IF;
END ofoa_auth;
/

  CREATE OR REPLACE FUNCTION "EMAIL_PRESENT" (p_email IN VARCHAR2)
RETURN NUMBER
AS
  l_emails NUMBER(1) := 0;
BEGIN
  SELECT COUNT(*) INTO l_emails
  FROM clients
  WHERE email = p_email;
  IF l_emails > 0 THEN
    RETURN l_emails;
  END IF;

  SELECT COUNT(*) INTO l_emails
  FROM restaurants
  WHERE email = p_email;
  RETURN l_emails;
END email_present;
/

  CREATE OR REPLACE FUNCTION "CART_INSERT" (p_restaurant_id IN NUMBER, p_client_id IN NUMBER, p_product_id IN NUMBER, p_amount IN NUMBER)
RETURN NUMBER
AS
  l_result NUMBER := 0;
BEGIN
    SELECT COUNT(*) INTO l_result
    FROM products
    WHERE product_id = p_product_id AND restaurant_id = p_restaurant_id;
    IF l_result = 0 THEN
      RETURN l_result;
    END IF;

    DELETE FROM cart
    WHERE client_id = p_client_id AND product_id = p_product_id;

    INSERT INTO cart (client_id, product_id, amount)
    VALUES (p_client_id, p_product_id, p_amount);
    RETURN 1;
END cart_insert;
/
