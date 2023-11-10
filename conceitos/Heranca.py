class Funcionario():
    def __init_(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def dados(self):
        return { 'nome': self.nome, 'salário': self.salario }
    
class Admin(Funcionario):
    def __init__(self, nome, salario):
        super().__init_(nome, salario)
    
    def atualizarDados(self, nome):
        self.nome = nome
        return self.dados()

fabio = Funcionario('Fabio', 7000)

fabio.dados()

fernando = Admin('Fernando', 14000)

fernando.atualizarDados('Fernandinho')