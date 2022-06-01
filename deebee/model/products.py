# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelProducts(Model):
  def __init__(self, conn, restaurant_id):
    Model.__init__(self, conn)
    self.restaurant_id = restaurant_id

  def list_products(self):
    SQL = """
    SELECT product_id, name, description, price
    FROM products
    WHERE restaurant_id = :restaurant_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.restaurant_id])
      return ("Product ID", "Name", "Description", "Price"), cursor.fetchall()

  def add_product(self, name, description, price):
    SQL = """
    INSERT INTO products (restaurant_id, name, description, price)
    VALUES (:restaurant_id, :name, :description, :price)
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.restaurant_id, name, description, price])
      self.conn.commit()

  def delete_product(self, product_id):
    SQL = """
    DELETE FROM products
    WHERE restaurant_id = :restaurant_id AND product_id = :product_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.restaurant_id, product_id])
      self.conn.commit()

  def add_to_cart(self, client_id, product_id, amount):
    with self.conn.cursor() as cursor:
      result = cursor.callfunc("cart_insert", int, [self.restaurant_id, client_id, product_id, amount])
      self.conn.commit()
