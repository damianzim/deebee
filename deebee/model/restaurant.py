# vim: ts=2 sts=0 sw=2 tw=120 et

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

  @staticmethod
  def register(conn, name, email, password, phone_number, street_address, postal_code, city, food_type_id):
    SQL = """
    INSERT
      INTO restaurants (name, email, password, phone_number, street_address, postal_code, city, food_type_id)
      VALUES (:name, :email, :password, :phone_number, :street_address, :postal_code, :city, :food_type_id)
    """
    with conn.cursor() as cursor:
      emails = cursor.callfunc("email_present", int, [email])
      if emails != 0:
        print("Error: Register restaurant: Email is already in use")
        return False
      cursor.execute(SQL, [name, email, password, phone_number, street_address, postal_code, city, food_type_id])
      conn.commit()
    return True
