def meu_metodo(arg1, arg2):
    return arg1 + arg2

def meu_metodo_longo(arg1, arg2, arg3, arg4, arg5):
    return arg1 + arg2 + arg3 + arg4 + arg5

def minha_lista_somada(lista):
    return sum(lista)

def soma_simplificada(*args):
    return sum(*args)

def metodos_kwargs(*args, **kwargs):
    print(args)
    print(kwargs)

print(meu_metodo(5, 6))
print(meu_metodo_longo(2, 3, 4, 5, 6))
print(minha_lista_somada([3, 6, 5, 1]))
print(soma_simplificada(3, 6, 5, 1))
print(metodos_kwargs(3, 'teste', 10, 'frase',idade=15))