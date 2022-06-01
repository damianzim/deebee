# vim: ts=2 sts=0 sw=2 tw=120 et

from deebee.model.model import Model

class ModelReviews(Model):
  def __init__(self, conn, restaurant_id):
    Model.__init__(self, conn)
    self.restaurant_id = restaurant_id

  def list_reviews(self):
    SQL = """
    SELECT r.review_id, r.rating, r.content AS review_content, rr.content AS reply_content
    FROM reviews r
    LEFT JOIN review_replies rr
      ON r.review_id = rr.review_id
    WHERE r.restaurant_id = :restaurant_id
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, [self.restaurant_id])
      return ("Rewview ID", "Rating", "Review content", "Reply content"), cursor.fetchall()

  def add_review(self, client_id, rating, content):
    with self.conn.cursor() as cursor:
      result = cursor.callfunc("place_review", int, [self.restaurant_id, client_id, rating, content])
      self.conn.commit()
      if result == 0:
        print("Error: Cannot place review, number of orders in this restaurant is not grater than the number of",
          "placed reviews")
      else:
        print("Info: Review has been placed")

  def review_reply(self, review_id, content):
    SQL = """
    INSERT INTO review_replies (review_id, content)
    SELECT :review_id, :content
    FROM dual
    WHERE (SELECT restaurant_id
           FROM reviews
           WHERE review_id = :review_id) = :restaurant_id AND NOT EXISTS (SELECT review_reply_id
                                                                          FROM review_replies
                                                                          WHERE review_id = :review_id)
    """
    with self.conn.cursor() as cursor:
      cursor.execute(SQL, review_id=review_id, content=content, restaurant_id=self.restaurant_id)
      self.conn.commit()
