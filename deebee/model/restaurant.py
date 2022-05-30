# vim: ts=2 sts=0 sw=2 tw=100 et

from deebee.model.model import Model, dataclass

@dataclass
class ModelRestaurant(Model):
  client_id: int
  name: str
  email: str
  phone_number: str
  street_address: str
  postal_code: str
  city: str
  food_type_id: int
  defunct: str

  @staticmethod
  def login(conn, email):
    SQL = """
    SELECT restaurant_id, name, email, phone_number, street_address, postal_code, city, food_type_id, defunct
    FROM restaurants
    WHERE email = :email
    """
    with conn.cursor() as cursor:
      cursor.execute(SQL, email=email)
      row = cursor.fetchone()
    if row is None:
      return None
    return ModelRestaurant(conn, *row)
