from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp

from models.User import UserModel
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        
        if user:
            return user.json()
        
        return { 'message': 'User not exists!' }, 404
    
    @jwt_required
    def delete(self, user_id):        
        user = UserModel.find_user(user_id)
        
        if not user:
            return { 'message': "User not exists" }, 404
        
        try:
            user.delete_user()
        
            return { 'message': 'User Deleted' }, 200
        except:
            return { 'message': 'An internal error ocurred trying to delete user!' }, 500

class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        
        if UserModel.find_by_login(dados['login']):
            return { "message": f"The login {dados['login']} already exists!" }, 400
        
        user = UserModel(**dados)
        
        user.save_user()
        
        return { "message": "User created!!" }

class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UserModel.find_by_login(dados['login'])
        
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            
            return { 'access_token': token_de_acesso }, 200
        
        return { "message": "Login or Password incorrect" }, 401
    
class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)

        return { "message": "Logged out successfully!" }, 200