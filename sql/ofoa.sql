--------------------------------------------------------
-- Online Food Ordering Application
--------------------------------------------------------

--------------------------------------------------------
-- Drop tables (also drops triggers)
--------------------------------------------------------
  DROP TABLE "PRODUCTS" cascade constraints;
  DROP TABLE "ORDERS" cascade constraints;
  DROP TABLE "ORDER_DETAILS" cascade constraints;
  DROP TABLE "CLIENTS" cascade constraints;
  DROP TABLE "CART" cascade constraints;
  DROP TABLE "FOOD_TYPES" cascade constraints;
  DROP TABLE "RESTAURANTS" cascade constraints;
  DROP TABLE "FAVORITES" cascade constraints;
  DROP TABLE "REVIEWS" cascade constraints;
  DROP TABLE "REVIEW_REPLIES" cascade constraints;


--------------------------------------------------------
-- Drop sequencees
--------------------------------------------------------
  DROP SEQUENCE "PRODUCT_SEQ";
  DROP SEQUENCE "ORDER_SEQ";
  DROP SEQUENCE "ORDER_DETAIL_SEQ";
  DROP SEQUENCE "CLIENT_SEQ";
  DROP SEQUENCE "CART_ENTRY_SEQ";
  DROP SEQUENCE "FOOD_TYPE_SEQ";
  DROP SEQUENCE "RESTAURANT_SEQ";
  DROP SEQUENCE "FAV_ENTRY_SEQ";
  DROP SEQUENCE "REVIEW_SEQ";
  DROP SEQUENCE "REVIEW_REPLY_SEQ";


--------------------------------------------------------
-- Drop views
--------------------------------------------------------
  DROP VIEW "PRODUCT_DETAILS_VIEW";


--------------------------------------------------------
-- Create sequences
--------------------------------------------------------
  CREATE SEQUENCE "PRODUCT_SEQ";
  CREATE SEQUENCE "ORDER_SEQ";
  CREATE SEQUENCE "ORDER_DETAIL_SEQ";
  CREATE SEQUENCE "CLIENT_SEQ";
  CREATE SEQUENCE "CART_ENTRY_SEQ";
  CREATE SEQUENCE "FOOD_TYPE_SEQ";
  CREATE SEQUENCE "RESTAURANT_SEQ";
  CREATE SEQUENCE "FAV_ENTRY_SEQ";
  CREATE SEQUENCE "REVIEW_SEQ";
  CREATE SEQUENCE "REVIEW_REPLY_SEQ";


--------------------------------------------------------
-- Create table: PRODUCTS
--------------------------------------------------------
  CREATE TABLE "PRODUCTS"
  (
    "PRODUCT_ID" NUMBER(6,0) NOT NULL,
    "RESTAURANT_ID" NUMBER(4,0), -- May be NULL is restaurant deletes this product.
    "NAME" VARCHAR2(30 BYTE) NOT NULL,
    "DESCRIPTION" VARCHAR2(200 BYTE) NOT NULL,
    "PRICE" NUMBER(5,2) NOT NULL CHECK ("PRICE" > 0)
  );

  ALTER TABLE "PRODUCTS" ADD CONSTRAINT "PRODUCT_ID_PK" PRIMARY KEY ("PRODUCT_ID");


--------------------------------------------------------
-- Create table: ORDERS
--------------------------------------------------------
  CREATE TABLE "ORDERS"
  (
    "ORDER_ID" NUMBER(8,0) NOT NULL,
    "CLIENT_ID" NUMBER(6,0) NOT NULL,
    "RESTAURANT_ID" NUMBER(4,0) NOT NULL,
    "STATE" VARCHAR2(10 BYTE) CHECK("STATE" IN ('Checkout', 'Pending', 'Completed')) NOT NULL,
    "ORDER_DATE" DATE NOT NULL
  );

  ALTER TABLE "ORDERS" ADD CONSTRAINT "ORDER_ID_PK" PRIMARY KEY ("ORDER_ID");


--------------------------------------------------------
-- Create table: ORDER_DETAILS
--------------------------------------------------------
  CREATE TABLE "ORDER_DETAILS"
  (
    "ORDER_DETAIL_ID" NUMBER(10,0) NOT NULL,
    "ORDER_ID" NUMBER(8,0) NOT NULL,
    "PRODUCT_ID" NUMBER(6,0) NOT NULL,
    "AMOUNT" NUMBER(1,0) NOT NULL CHECK ("AMOUNT" >= 1)
  );

  ALTER TABLE "ORDER_DETAILS" ADD CONSTRAINT "ORDER_DETAIL_ID_PK" PRIMARY KEY ("ORDER_DETAIL_ID");


--------------------------------------------------------
-- Create table: CLIENTS
--------------------------------------------------------
  CREATE TABLE "CLIENTS"
  (
    "CLIENT_ID" NUMBER(6,0) NOT NULL,
    "FIRST_NAME" VARCHAR2(20 BYTE) NOT NULL,
    "LAST_NAME" VARCHAR2(25 BYTE) NOT NULL,
    "EMAIL" VARCHAR2(50 BYTE) NOT NULL UNIQUE,
    "PASSWORD" RAW(32) NOT NULL, -- SHA256
    "PHONE_NUMBER" VARCHAR2(20 BYTE) UNIQUE,
    "STREET_ADDRESS" VARCHAR2(40 BYTE) NOT NULL,
    "POSTAL_CODE" VARCHAR2(12 BYTE) NOT NULL,
    "CITY" VARCHAR2(30 BYTE) NOT NULL
  );

  ALTER TABLE "CLIENTS" ADD CONSTRAINT "CLIENT_ID_PK" PRIMARY KEY ("CLIENT_ID");


--------------------------------------------------------
-- Create table: CART
--------------------------------------------------------
  CREATE TABLE "CART"
  (
    "CART_ENTRY_ID" NUMBER(8,0) NOT NULL,
    "CLIENT_ID" NUMBER(6,0) NOT NULL,
    "PRODUCT_ID" NUMBER(6,0) NOT NULL,
    "AMOUNT" NUMBER(1,0) NOT NULL CHECK ("AMOUNT" >= 1)
  );

  ALTER TABLE "CART" ADD CONSTRAINT "CART_ENTRY_ID_PK" PRIMARY KEY ("CART_ENTRY_ID");


--------------------------------------------------------
-- Create table: FOOD_TYPES
--------------------------------------------------------
  CREATE TABLE "FOOD_TYPES"
  (
    "FOOD_TYPE_ID" NUMBER(2,0) NOT NULL,
    "NAME" VARCHAR2(20 BYTE) NOT NULL UNIQUE
  );

  ALTER TABLE "FOOD_TYPES" ADD CONSTRAINT "FOOD_TYPE_ID_PK" PRIMARY KEY ("FOOD_TYPE_ID");


--------------------------------------------------------
-- Create table: RESTAURANTS
--------------------------------------------------------
  CREATE TABLE "RESTAURANTS"
  (
    "RESTAURANT_ID" NUMBER(4,0) NOT NULL,
    "NAME" VARCHAR2(20 BYTE) NOT NULL UNIQUE,
    "EMAIL" VARCHAR2(50 BYTE) NOT NULL UNIQUE,
    "PASSWORD" RAW(32) NOT NULL, -- SHA256
    "PHONE_NUMBER" VARCHAR2(20 BYTE) UNIQUE,
    "STREET_ADDRESS" VARCHAR2(40 BYTE) NOT NULL,
    "POSTAL_CODE" VARCHAR2(12 BYTE) NOT NULL,
    "CITY" VARCHAR2(30 BYTE) NOT NULL,
    "FOOD_TYPE_ID" NUMBER(2,0) NOT NULL,
    "DEFUNCT" CHAR(1) DEFAULT 'n' CHECK("DEFUNCT" IN ('y','n')) NOT NULL
  );

  ALTER TABLE "RESTAURANTS" ADD CONSTRAINT "RESTAURANT_ID_PK" PRIMARY KEY ("RESTAURANT_ID");


--------------------------------------------------------
-- Create table: FAVORITES
--------------------------------------------------------
  CREATE TABLE "FAVORITES"
  (
    "FAV_ENTRY_ID" NUMBER(8,0) NOT NULL,
    "CLIENT_ID" NUMBER(6,0) NOT NULL,
    "RESTAURANT_ID" NUMBER(4,0) NOT NULL
  );

  ALTER TABLE "FAVORITES" ADD CONSTRAINT "FAV_ENTRY_ID_PK" PRIMARY KEY ("FAV_ENTRY_ID");


--------------------------------------------------------
-- Create table: REVIEWS
--------------------------------------------------------
  CREATE TABLE "REVIEWS"
  (
    "REVIEW_ID" NUMBER(8,0) NOT NULL,
    "RESTAURANT_ID" NUMBER(4,0) NOT NULL,
    "CLIENT_ID" NUMBER(6,0), -- Anonymous review??
    "CONTENT" VARCHAR2(200 BYTE) NOT NULL,
    "RATING" NUMBER(1,0) NOT NULL CHECK ("RATING" BETWEEN 1 AND 5)
  );

  ALTER TABLE "REVIEWS" ADD CONSTRAINT "REVIEW_ID_PK" PRIMARY KEY ("REVIEW_ID");


--------------------------------------------------------
-- Create table: REVIEW_REPLIES
--------------------------------------------------------
  CREATE TABLE "REVIEW_REPLIES"
  (
    "REVIEW_REPLY_ID" NUMBER(8,0) NOT NULL,
    "REVIEW_ID" NUMBER(8,0) NOT NULL,
    "CONTENT" VARCHAR2(200 BYTE) NOT NULL
  );

  ALTER TABLE "REVIEW_REPLIES" ADD CONSTRAINT "REVIEW_REPLY_ID_PK" PRIMARY KEY ("REVIEW_REPLY_ID");


--------------------------------------------------------
--  DDL for View PRODUCT_DETAILS_VIEW
--------------------------------------------------------

  CREATE OR REPLACE FORCE VIEW "PRODUCT_DETAILS_VIEW" ("PRODUCT_ID", "RESTAURANT_ID", "RESTAURANT_NAME", "NAME", "DESCRIPTION", "PRICE") AS
    SELECT p.product_id, p.restaurant_id, r.name, p.name, p.description, p.price
    FROM products p INNER JOIN restaurants r ON p.restaurant_id = r.restaurant_id
    WITH READ ONLY;


--------------------------------------------------------
-- Trigger for sequence: PRODUCT_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "PRODUCT_ON_INSERT"
    BEFORE INSERT ON products
    FOR EACH ROW
BEGIN
  SELECT PRODUCT_SEQ.nextval
  INTO :new.PRODUCT_ID
  FROM dual;
END product_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: ORDER_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "ORDER_ON_INSERT"
    BEFORE INSERT ON orders
    FOR EACH ROW
BEGIN
  SELECT ORDER_SEQ.nextval
  INTO :new.ORDER_ID
  FROM dual;
END order_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: ORDER_STATE_ON_ORDER
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "ORDER_STATE_ON_ORDER"
    BEFORE INSERT ON orders
    FOR EACH ROW
BEGIN
  :new.STATE := 'Checkout';
END order_state_on_order;
/


--------------------------------------------------------
-- Trigger for sequence: ORDER_ORDER_DATE_ON_ORDER
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "ORDER_ORDER_DATE_ON_ORDER"
    BEFORE UPDATE OR INSERT ON orders
    FOR EACH ROW
BEGIN
  :new.ORDER_DATE := sysdate;
END order_order_date_on_order;
/


--------------------------------------------------------
-- Trigger for sequence: ORDER_DETAIL_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "ORDER_DETAIL_ON_INSERT"
    BEFORE INSERT ON order_details
    FOR EACH ROW
BEGIN
  SELECT ORDER_DETAIL_SEQ.nextval
  INTO :new.ORDER_DETAIL_ID
  FROM dual;
END order_detail_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: CLIENT_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "CLIENT_ON_INSERT"
    BEFORE INSERT ON clients
    FOR EACH ROW
BEGIN
  SELECT CLIENT_SEQ.nextval
  INTO :new.CLIENT_ID
  FROM dual;
END client_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: CART_ENTRY_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "CART_ENTRY_ON_INSERT"
    BEFORE INSERT ON cart
    FOR EACH ROW
BEGIN
  SELECT CART_ENTRY_SEQ.nextval
  INTO :new.CART_ENTRY_ID
  FROM dual;
END cart_entry_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: FOOD_TYPE_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "FOOD_TYPE_ON_INSERT"
    BEFORE INSERT ON food_types
    FOR EACH ROW
BEGIN
  SELECT FOOD_TYPE_SEQ.nextval
  INTO :new.FOOD_TYPE_ID
  FROM dual;
END food_type_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: RESTAURANT_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "RESTAURANT_ON_INSERT"
    BEFORE INSERT ON restaurants
    FOR EACH ROW
BEGIN
  SELECT RESTAURANT_SEQ.nextval
  INTO :new.RESTAURANT_ID
  FROM dual;
END restaurant_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: FAV_ENTRY_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "FAV_ENTRY_ON_INSERT"
    BEFORE INSERT ON favorites
    FOR EACH ROW
BEGIN
  SELECT FAV_ENTRY_SEQ.nextval
  INTO :new.FAV_ENTRY_ID
  FROM dual;
END fav_entry_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: REVIEW_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "REVIEW_ON_INSERT"
    BEFORE INSERT ON reviews
    FOR EACH ROW
BEGIN
  SELECT REVIEW_SEQ.nextval
  INTO :new.REVIEW_ID
  FROM dual;
END review_on_insert;
/


--------------------------------------------------------
-- Trigger for sequence: REVIEW_REPLY_SEQ
--------------------------------------------------------
  CREATE OR REPLACE TRIGGER "REVIEW_REPLY_ON_INSERT"
    BEFORE INSERT ON review_replies
    FOR EACH ROW
BEGIN
  SELECT REVIEW_REPLY_SEQ.nextval
  INTO :new.REVIEW_REPLY_ID
  FROM dual;
END review_reply_on_insert;
/


--------------------------------------------------------
--  Ref Constraints for Table PRODUCTS
--------------------------------------------------------
  ALTER TABLE "PRODUCTS" ADD CONSTRAINT "PRODUCTS_RESTAURANT_ID_FK" FOREIGN KEY ("RESTAURANT_ID")
    REFERENCES "RESTAURANTS" ("RESTAURANT_ID") ENABLE;


--------------------------------------------------------
--  Ref Constraints for Table ORDERS
--------------------------------------------------------
  ALTER TABLE "ORDERS" ADD CONSTRAINT "ORDERS_CLIENT_ID_FK" FOREIGN KEY ("CLIENT_ID")
    REFERENCES "CLIENTS" ("CLIENT_ID") ENABLE;
  ALTER TABLE "ORDERS" ADD CONSTRAINT "ORDERS_RESTAURANT_ID_FK" FOREIGN KEY ("RESTAURANT_ID")
    REFERENCES "RESTAURANTS" ("RESTAURANT_ID") ENABLE;


--------------------------------------------------------
--  Ref Constraints for Table ORDER_DETAILS
--------------------------------------------------------
  ALTER TABLE "ORDER_DETAILS" ADD CONSTRAINT "ORDER_DETAILS_ORDER_ID_FK" FOREIGN KEY ("ORDER_ID")
    REFERENCES "ORDERS" ("ORDER_ID") ENABLE;
  ALTER TABLE "ORDER_DETAILS" ADD CONSTRAINT "ORDER_DETAILS_PRODUCT_ID_FK" FOREIGN KEY ("PRODUCT_ID")
    REFERENCES "PRODUCTS" ("PRODUCT_ID") ENABLE;


--------------------------------------------------------
--  Ref Constraints for Table CART
--------------------------------------------------------
  ALTER TABLE "CART" ADD CONSTRAINT "CART_CLIENT_ID_FK" FOREIGN KEY ("CLIENT_ID")
    REFERENCES "CLIENTS" ("CLIENT_ID") ENABLE;
  ALTER TABLE "CART" ADD CONSTRAINT "CART_PRODUCT_ID_FK" FOREIGN KEY ("PRODUCT_ID")
    REFERENCES "PRODUCTS" ("PRODUCT_ID") ENABLE;


--------------------------------------------------------
-- Ref Constraints for Table RESTAURANTS
--------------------------------------------------------
  ALTER TABLE "RESTAURANTS" ADD CONSTRAINT "FOOD_TYPE_ID_FK" FOREIGN KEY ("FOOD_TYPE_ID")
    REFERENCES "FOOD_TYPES" ("FOOD_TYPE_ID") ENABLE;

--------------------------------------------------------
--  Ref Constraints for Table FAVORITES
--------------------------------------------------------
  ALTER TABLE "FAVORITES" ADD CONSTRAINT "FAVORITES_CLIENT_ID_FK" FOREIGN KEY ("CLIENT_ID")
    REFERENCES "CLIENTS" ("CLIENT_ID") ENABLE;
  ALTER TABLE "FAVORITES" ADD CONSTRAINT "FAVORITES_RESTAURANT_ID_FK" FOREIGN KEY ("RESTAURANT_ID")
    REFERENCES "RESTAURANTS" ("RESTAURANT_ID") ENABLE;


--------------------------------------------------------
--  Ref Constraints for Table REVIEWS
--------------------------------------------------------
  ALTER TABLE "REVIEWS" ADD CONSTRAINT "REVIEWS_RESTAURANT_ID_FK" FOREIGN KEY ("RESTAURANT_ID")
    REFERENCES "RESTAURANTS" ("RESTAURANT_ID") ENABLE;
  ALTER TABLE "REVIEWS" ADD CONSTRAINT "REVIEWS_CLIENT_ID_FK" FOREIGN KEY ("CLIENT_ID")
    REFERENCES "CLIENTS" ("CLIENT_ID") ENABLE;


--------------------------------------------------------
--  Ref Constraints for Table REVIEW_REPLIES
--------------------------------------------------------
  ALTER TABLE "REVIEW_REPLIES" ADD CONSTRAINT "REVIEW_REPLIES_REVIEW_ID_FK" FOREIGN KEY ("REVIEW_ID")
    REFERENCES "REVIEWS" ("REVIEW_ID") ENABLE;


--------------------------------------------------------
-- Insert Into Table FOOD_TYPES
--------------------------------------------------------
  INSERT INTO food_types (name) VALUES ('Italian');
  INSERT INTO food_types (name) VALUES ('Kebap');
  INSERT INTO food_types (name) VALUES ('American');
  INSERT INTO food_types (name) VALUES ('Indian');
  INSERT INTO food_types (name) VALUES ('Other');


--------------------------------------------------------
-- Examplary records
--------------------------------------------------------
INSERT
  INTO restaurants (name, email, password, phone_number, street_address, postal_code, city, food_type_id)
  VALUES ('Pepperoni', 'contact@pepperoni.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', '+48 123 456 789', 'Al. Jerozolimskie 18/2', '00-375', 'Warszawa', (SELECT food_type_id FROM food_types WHERE name = 'Italian'));

INSERT INTO products (restaurant_id, name, description, price) VALUES (1, 'Pizza Margherita', 'Size: S, Components: cheese', 24.5);
INSERT INTO products (restaurant_id, name, description, price) VALUES (1, 'Pizza Margherita', 'Size: L, Components: cheese', 30);
INSERT INTO products (restaurant_id, name, description, price) VALUES (1, 'Pizza Margherita', 'Size: XL, Components: cheese', 35);
INSERT INTO products (restaurant_id, name, description, price) VALUES (1, 'Pizza Pepperoni', 'Size: S, Components: cheese, pepperoni, onion, extra virgin olive', 28.5);
INSERT INTO products (restaurant_id, name, description, price) VALUES (1, 'Pizza Pepperoni', 'Size: L, Components: cheese, pepperoni, onion, extra virgin olive', 34);
INSERT INTO products (restaurant_id, name, description, price) VALUES (1, 'Pizza Pepperoni', 'Size: XL, Components: cheese, pepperoni, onion, extra virgin olive', 40);

INSERT
  INTO restaurants (name, email, password, phone_number, street_address, postal_code, city, food_type_id)
  VALUES ('Antalya', 'contact@antalya.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', '+48 789 654 312', 'Al. Jerozolimskie 312', '00-375', 'Warszawa', (SELECT food_type_id FROM food_types WHERE name = 'Kebap'));

INSERT
  INTO clients (first_name, last_name, email, password, street_address, postal_code, city)
  VALUES ('Bob', 'Williams', 'bob@williams.com', hextoraw('0700a58f2e604b685c61b06ba145fa31e2803a932b6a12dfedd8e36062e0e114'), 'Marszałkowska 501', '00-123', 'Warszawa');
INSERT
  INTO clients (first_name, last_name, email, password, street_address, postal_code, city)
  VALUES ('John', 'Williams', 'john@williams.com', hextoraw('0700a58f2e604b685c61b06ba145fa31e2803a932b6a12dfedd8e36062e0e114'), 'Marszałkowska 501', '00-123', 'Warszawa');

INSERT INTO favorites (client_id, restaurant_id) VALUES (1, 1);
INSERT INTO favorites (client_id, restaurant_id) VALUES (1, 2);

  DECLARE
    l_order_id NUMBER(8);
BEGIN
  INSERT INTO orders (client_id, restaurant_id) VALUES (1, 1) RETURNING order_id INTO l_order_id;
  INSERT INTO order_details (order_id, product_id, amount) VALUES (l_order_id, 2, 1);
  INSERT INTO order_details (order_id, product_id, amount) VALUES (l_order_id, 4, 2);
END;
