from flask_restful import Resource, reqparse

from models.User import UserModel

class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        
        if user:
            return user.json()
        
        return { 'message': 'User not exists!' }, 404
    
    def delete(self, user_id):        
        user = UserModel.find_user(user_id)
        
        if not user:
            return { 'message': "User not exists" }, 404
        
        try:
            user.delete_user()
        
            return { 'message': 'User Deleted' }, 200
        except:
            return { 'message': 'An internal error ocurred trying to delete user!' } , 500
    