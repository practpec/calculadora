import pydot
from lark.tree import Tree
import os
import logging

logger = logging.getLogger(__name__)

# Directorio para guardar imágenes generadas
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    logger.debug("Ruta absoluta de IMAGE_DIR: %s", os.path.abspath(IMAGE_DIR))


def tree_to_pydot(tree: Tree) -> pydot.Dot:
    """
    Convierte un árbol de Lark a un objeto Pydot para su visualización.
    """
    graph = pydot.Dot(graph_type='graph')
    node_id = 0

    def add_nodes_edges(node, parent=None):
        nonlocal node_id
        current_id = node_id
        if isinstance(node, Tree):
            node_label = node.data
            graph.add_node(pydot.Node(str(current_id), label=node_label))
            if parent is not None:
                graph.add_edge(pydot.Edge(str(parent), str(current_id)))
            node_id += 1
            for child in node.children:
                add_nodes_edges(child, current_id)
        else:
            node_label = str(node)
            graph.add_node(pydot.Node(str(current_id), label=node_label, shape='ellipse'))
            if parent is not None:
                graph.add_edge(pydot.Edge(str(parent), str(current_id)))
            node_id += 1

    add_nodes_edges(tree)
    return graph

def visualizar_arbol(tree: Tree, nombre_archivo: str = "arbol_expresion.png") -> str:
    """
    Genera una imagen PNG del árbol de análisis sintáctico usando Graphviz.
    Retorna la ruta relativa de la imagen para servirla en la web.
    """
    try:
        graph = tree_to_pydot(tree)
        filename = "arbol.png"
        image_path = os.path.join(IMAGE_DIR, filename)
        graph.write_png(image_path)
        logger.debug("Árbol guardado como %s", filename)
        return f"images/{filename}"
    except Exception as e:
        logger.error("Error al generar la imagen del árbol: %s", e)
        return None
