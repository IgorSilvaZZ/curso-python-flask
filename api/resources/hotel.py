import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.Hotel import HotelModel

def normalize_path_params(
    cidade=None,
    estrelas_min=0,
    estrelas_max=5,
    diaria_min=0,
    diaria_max=10000,
    limit=50,
    offset=0,
    **dados
):
    if cidade:
        return {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "cidade": cidade,
            "limit": limit,
            "offset": offset
        }
    
    return {
        "estrelas_min": estrelas_min,
        "estrelas_max": estrelas_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "limit": limit,
        "offset": offset
    }

query_params = reqparse.RequestParser()
query_params.add_argument('cidade', type=str)
query_params.add_argument('estrelas_min', type=float)
query_params.add_argument('estrelas_max', type=float)
query_params.add_argument('diaria_min', type=float)
query_params.add_argument('diaria_max', type=float)
query_params.add_argument('limit', type=float)
query_params.add_argument('offset', type=float)

class Hoteis(Resource):
    def get(self):

        connection = sqlite3.connect('dev.db')
        cursor = connection.cursor()

        query = query_params.parse_args()

        query_validate = {key: query[key] for key in query if query[key] is not None}

        params = normalize_path_params(**query_validate)

        if not params.get('cidade'):
            consulta = "SELECT * FROM hoteis WHERE (estrelas >= ? AND estrelas <= ?) AND (diaria > ? AND diaria < ?) LIMIT ? OFFSET ?"

            tupla = tuple([params[key] for key in params]) # (estrelas_min, estrelas_max, diaria_min, diaria_max, limit, offset)

            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM hoteis WHERE (estrelas >= ? AND estrelas <= ?) AND (diaria > ? AND diaria < ?) AND cidade = ? LIMIT ? OFFSET ?"

            tupla = tuple([params[key] for key in params]) # (estrelas_min, estrelas_max, diaria_min, diaria_max, limit, offset)

            resultado = cursor.execute(consulta, tupla)

        hoteis = []

        for linha in resultado:
            # linha [hotel_id, nome, estrelas, diaria, cidade]

            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })

        return {
            'hoteis': hoteis
        }
        
class Hotel(Resource):
    def parse_args():
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank!")
        argumentos.add_argument('estrelas', type=float, required=True, help="The fiield 'estrelas' cannot be left blank!")
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')
        
        dados = argumentos.parse_args()
        
        return dados
    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:
            return hotel.json()
            
        return { 'message': "Hotel not exists!" }, 404
    
    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return { 'message': f"Hotel id {hotel_id} already exists!" }, 400
        
        dados = Hotel.parse_args()
        
        hotel = HotelModel(hotel_id, **dados)
        
        try:
            hotel.save_hotel()
        
            return hotel.json(), 201
        except:
            return { 'message': 'An internal error ocurred trying to save hotel!' } , 500      
        
    def put(self, hotel_id):
        dados = Hotel.parse_args()
        
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        
        novo_hotel = HotelModel(hotel_id, **dados)
        
        try:
            novo_hotel.save_hotel()
        
            return novo_hotel.json(), 201
        except:
            return { 'message': 'An internal error ocurred trying to save hotel!' } , 500
    
    def delete(self, hotel_id):        
        hotel = HotelModel.find_hotel(hotel_id)
        
        if not hotel:
            return { 'message': "Hotel not exists" }, 400
        
        try:
            hotel.delete_hotel()
        
            return { 'message': 'Hotel Deleted' }, 200
        except:
            return { 'message': 'An internal error ocurred trying to delete hotel!' } , 500