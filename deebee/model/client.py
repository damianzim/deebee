# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model, dataclass

@dataclass
class ModelClient(Model):
  client_id: int
  first_name: str
  last_name: str
  email: str
  phone_number: str
  street_address: str
  postal_code: str
  city: str

  @staticmethod
  def login(conn, email):
    SQL = """
    SELECT client_id, first_name, last_name, email, phone_number, street_address, postal_code, city
    FROM clients
    WHERE email = :email
    """
    with conn.cursor() as cursor:
      cursor.execute(SQL, email=email)
      row = cursor.fetchone()
    if row is None:
      return None
    return ModelClient(conn, *row)

  @staticmethod
  def register(conn, first_name, last_name, email, password, phone_number, street_address, postal_code, city):
    SQL = """
    INSERT
      INTO clients (first_name, last_name, email, password, phone_number, street_address, postal_code, city)
      VALUES (:first_name, :last_name, :email, :password, :phone_number, :street_address, :postal_code, :city)
    """
    with conn.cursor() as cursor:
      emails = cursor.callfunc("email_present", int, [email])
      if emails != 0:
        print("Error: Register client: Email is already in use")
        return False
      cursor.execute(SQL, [first_name, last_name, email, password, phone_number, street_address, postal_code, city])
      conn.commit()
    return True

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
