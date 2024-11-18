from flask import Flask, render_template, request  # Importar 'request' aquí
from .parser_module import parser
from .transformer_module import Calculadora
from .utils import visualizar_arbol
import logging

def create_app():
    app = Flask(__name__, static_folder='static')

    # Configurar el logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        resultado = None
        imagen = None
        expresion = ''

        if request.method == 'POST':
            expresion = request.form.get('expresion', '')
            if expresion:
                try:
                    # Parsear la expresión
                    tree = parser.parse(expresion)
                    logger.debug("Árbol de análisis sintáctico:\n%s", tree.pretty())

                    # Visualizar el árbol y obtener la ruta de la imagen
                    imagen = visualizar_arbol(tree)
                    logger.debug("Imagen generada: %s", imagen)

                    # Evaluar la expresión
                    calc = Calculadora()
                    resultado = calc.transform(tree)
                    print(imagen)

                    logger.debug("Resultado: %s", resultado)
                except Exception as e:
                    logger.error("Error al procesar la expresión: %s", e)
                    resultado = "Error en la expresión. Por favor, verifica la sintaxis."

        return render_template('index.html', resultado=resultado, imagen=imagen, expresion=expresion)

    return app
