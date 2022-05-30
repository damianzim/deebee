# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelFavorites(Model):
  def __init__(self, conn, client_id):
    Model.__init__(self, conn)
    self.client_id = client_id

  def add_fav_entry(self, restaurant_id):
    SQL = """
    INSERT INTO favorites (client_id, restaurant_id)
    SELECT :client_id, :restaurant_id
    FROM dual
    WHERE NOT EXISTS (SELECT client_id
                      FROM favorites
                      WHERE client_id = :client_id AND restaurant_id = :restaurant_id)
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, client_id=self.client_id, restaurant_id=restaurant_id)
      self.conn.commit()

  def delete_fav_entry(self, fav_entry_id):
    SQL = """
    DELETE FROM favorites
    WHERE client_id = :client_id AND fav_entry_id = :fav_entry_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.client_id, fav_entry_id])
      self.conn.commit()

  def list_favorites(self):
    SQL = """
    SELECT f.fav_entry_id, r.name, ft.name
    FROM favorites f
    INNER JOIN restaurants r
      ON f.restaurant_id = r.restaurant_id
      INNER JOIN food_types ft
        ON r.food_type_id = ft.food_type_id
    WHERE f.client_id = :client_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.client_id])
      return ("Favorite ID", "Name", "Food type"), cursor.fetchall()
