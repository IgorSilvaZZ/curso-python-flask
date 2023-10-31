import datetime

class Funcionario():
    aumento = 1.04

    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def dados(self):
        return { 'nome': self.nome, 'salário': self.salario }
    
    def aplicar_aumento(self):
        self.salario = self.salario * self.aumento

    @classmethod
    def definir_novo_aumento(cls, novo_aumento):
        cls.aumento = novo_aumento

    @staticmethod
    def dia_util(dia):
        if dia.weekday() == 5 or dia.weekday() == 6:
            return False
        return True

fabio = Funcionario('Fabio', 6000)

print(fabio.dados())

fabio.aplicar_aumento()

print(fabio.dados())

Funcionario.definir_novo_aumento(1.05)

minha_data = datetime.datetime.today().date()

print(minha_data)

print(Funcionario.dia_util(minha_data))