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
            'hoteis': hoteis
        }
        
class Hotel(Resource):
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
    
    def parse_args():
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')
        
        dados = argumentos.parse_args()
        
        return dados
    
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        
        if hotel:
            return hotel
            
        return { 'message': "Hotel não encontrado!" }, 404
    
    def post(self, hotel_id):
        dados = Hotel.parse_args()
        
        # Aqui o hotel é retornado em formato de objeto]
        # Formato que não da para ser retornado ou ser manipulado nas requisições
        hotel_model = HotelModel(hotel_id, **dados)
        
        # Aqui utilizamos o metodo criado para transformar de objeto para dicionario, formato valido para manipuilação
        novo_hotel = hotel_model.json()
        
        hoteis.append(novo_hotel)
        
        return novo_hotel, 200
    
    def put(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        
        dados = Hotel.parse_args()
        
        hotel_model = HotelModel(hotel_id, **dados)
        
        novo_hotel = hotel_model.json()
        
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        
        hoteis.append(novo_hotel)
        
        return novo_hotel, 201
    
    def delete(self, hotel_id):
        global hoteis
        
        hotel = Hotel.find_hotel(hotel_id)
        
        if not hotel:
            return { 'message': "Hotel not found" }, 400
        
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        
        return { 'message': 'Hotel Deleted' }, 200