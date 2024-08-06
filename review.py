from flask import Blueprint, request, make_response
from flask_restful import Api, Resource
from models import db, Review, Mechanic, User

review_bp = Blueprint('review_bp', __name__, url_prefix='/reviews')
review_api = Api(review_bp)

class Reviews(Resource):
    def get(self):
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(reviews, 200)
    
    def post(self):
        data = request.get_json()

        if not data or not data.get('feedback') or not data.get('rating') or not data.get('mechanic_id') or not data.get('user_id'):
            return {"message": "Required fields: feedback, rating, mechanic_id, user_id"}, 400

        mechanic = Mechanic.query.get(data['mechanic_id'])
        user = User.query.get(data['user_id'])

        if not mechanic or not user:
            return {"message": "Mechanic or User not found"}, 404

        new_review = Review(
            rating=data['rating'],
            feedback=data.get('feedback'),
            mechanic_id=data['mechanic_id'],
            user_id=data['user_id']
        )

        try:
            db.session.add(new_review)
            db.session.commit()
            return make_response(new_review.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating review", "error": str(e)}, 500

review_api.add_resource(Reviews, '/', strict_slashes=False)



class ReviewById(Resource):
    def get(self, id):
        review = Review.query.filter(Review.id == id).first()
        if not review:
            return {"message": "Review not found"}, 404
        return review.to_dict(), 200

    def patch(self, id):
        review = Review.query.get(id)
        if not review:
            return {"message": "Review not found"}, 404

        data = request.get_json()
        if 'rating' in data:
            review.rating = data['rating']
        if 'feedback' in data:
            review.feedback = data['feedback']
        try:
            db.session.commit()
            return review.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating review", "error": str(e)}, 500

    def delete(self, id):
        review = Review.query.get(id)
        if not review:
            return {"message": "Review not found"}, 404
        try:
            db.session.delete(review)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting review", "error": str(e)}, 500

review_api.add_resource(ReviewById, '/<int:id>')