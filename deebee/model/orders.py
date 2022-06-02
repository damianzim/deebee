# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelOrders(Model):
  def __init__(self, conn):
    Model.__init__(self, conn)

  def show_for_client(self, client_id):
    SQL = """
    SELECT o.order_id, r.name AS restaurant_name, o.order_date, COUNT(*) AS products_no, SUM(od.amount) AS items_no, SUM((p.price * od.amount)) AS total_price, o.state
    FROM orders o
    INNER JOIN order_details od
      ON o.order_id = od.order_id
      INNER JOIN products p
        ON od.product_id = p.product_id
        INNER JOIN restaurants r
          ON p.restaurant_id = r.restaurant_id
    WHERE o.client_id = :client_id
    GROUP BY o.order_id, r.name, o.order_date, o.state
    ORDER BY o.order_id ASC
    """
    HEADER = ("Order ID", "Restaurant name", "Order date", "Products no.", "Items no.", "Total price", "Order state")
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [client_id])
      return HEADER, cursor.fetchall()

  def check_owner(self, order_id, client_id):
    SQL = """
    SELECT COUNT(*)
    FROM orders
    WHERE order_id = :order_id AND client_id = :client_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [order_id, client_id])
      return cursor.fetchone()[0] > 0
