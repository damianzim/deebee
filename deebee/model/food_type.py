# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model, dataclass

@dataclass
class ModelFoodType(Model):
  food_type_id: int
  name: str

  @staticmethod
  def list_food_types(conn):
    SQL = """
    SELECT food_type_id, name
    FROM food_types
    """
    with conn.cursor() as cursor:
      cursor.execute(SQL)
      return cursor.fetchall()
