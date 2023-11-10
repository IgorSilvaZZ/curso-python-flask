import functools

def meu_decorador(funcao):
    @functools.wraps(funcao)
    def funcao_que_roda_essa_funcao():
        print('Embrulhando função no decorator')
        funcao()
        print('Fechando o embrulho')

    return funcao_que_roda_essa_funcao

@meu_decorador
def minha_funcao():
    print("Eu sou uma função!!")

minha_funcao()
