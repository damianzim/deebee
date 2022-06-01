# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelRestaurants(Model):
  def __init__(self, conn, client_id):
    Model.__init__(self, conn)
    self.client_id = client_id

  def list_restaurants(self):
    SQL = """
    SELECT r.restaurant_id, r.name, ft.name, f.client_id
    FROM restaurants r
    LEFT JOIN (SELECT client_id, restaurant_id
               FROM favorites
               WHERE client_id = :client_id) f
      ON r.restaurant_id = f.restaurant_id
      INNER JOIN food_types ft
        ON r.food_type_id = ft.food_type_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, client_id=self.client_id)
      rows = cursor.fetchall()
    return ("ID", "Name", "Food type", "Favorite"), [
      (*cols, "x" if favorite is not None else "")
      for *cols, favorite in rows]

  def exists(self, restaurant_id):
    SQL = """
    SELECT COUNT(*)
    FROM restaurants
    WHERE restaurant_id = :restaurant_id AND defunct = 'n'
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [restaurant_id])
      count, = cursor.fetchone()
      return count > 0
