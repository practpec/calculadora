from flask import Flask, render_template, request
from .parser_module import parser, contar_tokens, obtener_tokens
from .transformer_module import Calculadora
from .utils import visualizar_arbol
import logging

memoria = None

def create_app():
    app = Flask(__name__, static_folder='static')

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        global memoria
        resultado = None
        imagen = None
        expresion = ''
        total_numeros = 0
        total_operadores = 0
        tokens = [] 

        if request.method == 'POST':
            if request.form.get('memoria') and memoria is not None:
                expresion = str(memoria)
            else:
                expresion = request.form.get('expresion', '')

            if expresion:
                try:
                    total_numeros, total_operadores = contar_tokens(expresion)
                    tokens = obtener_tokens(expresion)
                    tree = parser.parse(expresion)
                    imagen = visualizar_arbol(tree)
                    calc = Calculadora()
                    resultado = calc.transform(tree)
                    memoria = resultado 
                except Exception as e:
                    resultado = "Error en la expresión. Por favor, verifica la sintaxis."

        return render_template('index.html', resultado=resultado, imagen=imagen,
                               expresion=expresion, total_numeros=total_numeros,
                               total_operadores=total_operadores, tokens=tokens, memoria=memoria)

    return app
