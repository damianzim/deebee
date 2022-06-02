# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelOrderDetails(Model):
  def __init__(self, conn, order_id):
    Model.__init__(self, conn)
    self.order_id = order_id

  def show_details(self):
    SQL = """
    SELECT p.name AS product_name, p.price, od.amount, (p.price * od.amount) AS total_price
    FROM order_details od
    INNER JOIN products p
      ON od.product_id = p.product_id
    WHERE od.order_id = :order_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.order_id])
      return ("Product name", "Price", "Amount", "Total price"), cursor.fetchall()
