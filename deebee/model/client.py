# vim: ts=2 sts=0 sw=2 tw=100 et

def list_restaurants(conn):
  QUERY = """
  SELECT r.restaurant_id, r.name, ft.name
  FROM restaurants r
  INNER JOIN food_types ft
    ON r.food_type_id = ft.food_type_id
  WHERE defunct = 'n'
  """
  with conn.cursor() as cursor:
    cursor.execute(QUERY)
    rows = cursor.fetchall()
  return ("ID", "Name", "Food type"), rows
