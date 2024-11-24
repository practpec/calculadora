from .lexer import lexer
from lark import Lark, Transformer, Tree

# Gramática extendida para incluir nodos de árbol
gramatica = """
    ?start: expr

    ?expr: expr "+" term   -> sumar
         | expr "-" term   -> restar
         | term

    ?term: term "*" factor -> multiplicar
         | term "/" factor -> dividir
         | factor

    ?factor: "(" expr ")"
           | NUMBER        -> numero

    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

parser = Lark(gramatica, parser='earley', debug=False)

# Clase para transformar y evaluar el árbol
class Calculadora(Transformer):
    def numero(self, n):
        return int(n[0])

    def sumar(self, args):
        return args[0] + args[1]

    def restar(self, args):
        return args[0] - args[1]

    def multiplicar(self, args):
        return args[0] * args[1]

    def dividir(self, args):
        if args[1] == 0:
            raise ZeroDivisionError("División entre cero")
        return args[0] / args[1]

# Contar tokens
def contar_tokens(data):
    lexer.input(data)
    tokens = list(lexer)
    total_numeros = len([tok for tok in tokens if tok.type == 'NUMBER'])
    total_operadores = len([tok for tok in tokens if tok.type in {'PLUS', 'MINUS', 'TIMES', 'DIVIDE'}])
    return total_numeros, total_operadores

def obtener_tokens(data):
    lexer.input(data)
    tokens = list(lexer)
    token_list = [f"{tok.type}: {tok.value}" for tok in tokens]
    return token_list
