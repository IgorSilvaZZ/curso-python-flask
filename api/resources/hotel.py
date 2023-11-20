from flask_restful import Resource, reqparse

from models.Hotel import HotelModel

hoteis = [
    { 'hotel_id': 'alpha', 'nome': 'Alpha Hotel', 'estrelas': 4.3, 'diaria': 420.34, 'cidade': "Rio de Janeiro" },
    { 'hotel_id': 'bravo', 'nome': 'Bravo Hotel', 'estrelas': 4.4, 'diaria': 380.90, 'cidade': "Santa Catarina" },
    { 'hotel_id': 'charlie', 'nome': 'Charlie Hotel', 'estrelas': 3.9, 'diaria': 320.20, 'cidade': "Santa Catarina" },
]

class Hoteis(Resource):
    def get(self):
        return {
            'hoteis': [hotel.json() for hotel in HotelModel.query.all()]
        }
        
class Hotel(Resource):
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
    
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