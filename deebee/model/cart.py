# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelCart(Model):
  def __init__(self, conn, client_id):
    Model.__init__(self, conn)
    self.client_id = client_id

  def show_cart(self):
    SQL = """
    SELECT cart_entry_id, restaurant_name, name, price, amount, total_price
    FROM cart_view
    WHERE client_id = :client_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.client_id])
      return ("Cart entry ID", "Restaurant name", "Product name", "Price", "Amount", "Total price"), cursor.fetchall()

  def unique_restaurants(self):
    SQL = """
    SELECT p.restaurant_id
    FROM cart c
    INNER JOIN products p
      ON c.product_id = p.product_id
    WHERE c.client_id = :client_id
    GROUP BY p.restaurant_id
    ORDER BY p.restaurant_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.client_id])
      return ("Restaurant ID"), cursor.fetchall()

  def place_order(self, restaurant_id):
    SQL = """
      DECLARE
        l_order_id NUMBER(8);
    BEGIN
      INSERT INTO orders (client_id, restaurant_id)
      VALUES (:client_id, :restaurant_id)
      RETURNING order_id INTO l_order_id;

      INSERT INTO order_details (order_id, product_id, amount)
      SELECT l_order_id, product_id, amount
      FROM cart
      WHERE client_id = :client_id AND product_id IN (SELECT product_id
                                                      FROM products
                                                      WHERE restaurant_id = :restaurant_id);

      DELETE FROM cart
      WHERE client_id = :client_id AND product_id IN (SELECT product_id
                                                      FROM products
                                                      WHERE restaurant_id = :restaurant_id);
    END;
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, client_id=self.client_id, restaurant_id=restaurant_id)
      self.conn.commit()
