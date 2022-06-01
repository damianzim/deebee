# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelReviews(Model):
  def __init__(self, conn, restaurant_id):
    Model.__init__(self, conn)
    self.restaurant_id = restaurant_id

  def list_reviews(self): # TODO: ADD REVIEW REPLY COLUMN
    SQL = """
    SELECT review_id, rating, content
    FROM reviews
    WHERE restaurant_id = :restaurant_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.restaurant_id])
      return ("Rewview ID", "Rating", "Content"), cursor.fetchall()

  def add_review(self, client_id, rating, content):
    with self.conn.cursor() as cursor:
      result = cursor.callfunc("place_review", int, [self.restaurant_id, client_id, rating, content])
      self.conn.commit()
      if result == 0:
        print("Error: Cannot place review, number of orders in this restaurant is not grater than the number of",
          "placed reviews")
      else:
        print("Info: Review has been placed")
