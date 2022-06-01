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
