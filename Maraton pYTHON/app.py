from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesaria para usar sesiones

class Pregunta:
    def __init__(self, texto, opciones, respuesta):
        self.texto = texto
        self.opciones = opciones
        self.respuesta = respuesta

    def a_diccionario(self):
        """Convierte el objeto Pregunta a un diccionario para su serialización."""
        return {
            'texto': self.texto,
            'opciones': self.opciones,
            'respuesta': self.respuesta
        }

    @staticmethod
    def desde_diccionario(diccionario):
        """Crea una instancia de Pregunta a partir de un diccionario."""
        return Pregunta(diccionario['texto'], diccionario['opciones'], diccionario['respuesta'])
    
def inicializar_tablero(n, m):
    # Inicializar el tablero con todas las casillas en negro ('N')
    tablero = [['N' for _ in range(m)] for _ in range(n)]
    
    for i in range(n):
        # Invertir las filas pares para crear el efecto serpiente
        if i % 2 == 0:
            tablero[i] = tablero[i][::-1]
    p = 0
    # Aplicar las reglas específicas para cambiar elementos a blanco
    for i in range(0,n):
        for j in range(0,m):
            if tablero[i ][j] == 'N':
                p = p + 1
            if p == 5 :
                tablero[i ][j] = 'O'
                p = 0
            col =  i +1
            if col % 2 == 0 and col % 4 != 0 :
                # Para filas divisibles por 2 pero no por 4, y no la última fila,
                # cambiar el último elemento de la SIGUIENTE fila a blanco
                if j < m-1:
                    tablero[i ][j] = 'B'  # Corrección: Usar -1 para acceder al último elemento
            elif col % 4 == 0:
                # Para filas divisibles por 4, excepto la primera fila,
                # cambiar el primer elemento de la fila actual a blanco
                if j > 0:
                    tablero[i][j] = 'B'  # Corrección: Acceder al primer elemento correctamente
            

    # Asegurar que la primera casilla sea blanca y la última casilla sea negra
    tablero[0][0] = 'B'  # Casilla de inicio como Blanca
    if n % 2 == 0:
        tablero[-1][0] = 'B'  # Para un número par de filas, la última casilla al inicio de la fila
    else:
        tablero[-1][-1] = 'B'  # Para un número impar de filas, la última casilla al final de la fila
    
    return tablero


def cargar_preguntas_desde_csv(archivo):
    preguntas = []
    df = pd.read_csv(archivo)
    df = df.dropna(subset=['preguntas'])  # Eliminar filas con valores NaN en la columna 'preguntas'
    for index, row in df.iterrows():
        pregunta = Pregunta(row['preguntas'], str(row['opciones']).strip('][').split(', '), row['respuesta'])
        preguntas.append(pregunta)
    return preguntas

@app.route('/actualizar_preguntas', methods=['GET'])
def actualizar_preguntas():
    # Cargar preguntas desde el archivo CSV y guardar en sesión como diccionarios
    preguntas_totales = cargar_preguntas_desde_csv('econ.csv')
    print(preguntas_totales)
    session['preguntas'] = [pregunta.a_diccionario() for pregunta in preguntas_totales]
    session['preguntas_restantes'] = session['preguntas'].copy()
    # Redireccionar al usuario a la página de inicio después de actualizar las preguntas
    return redirect(url_for('inicio'))

# Ruta inicial que muestra una pregunta aleatoria
@app.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    respuesta_seleccionada = request.form.get('opcion')
    pregunta_actual_diccionario = session.get('pregunta_actual', None)
    if pregunta_actual_diccionario:
        pregunta_actual_objeto = Pregunta.desde_diccionario(pregunta_actual_diccionario)
        if respuesta_seleccionada == pregunta_actual_objeto.respuesta:
            return jsonify(correcto=True, mensaje='¡Correcto! Has acertado la pregunta.')
        else:
            return jsonify(correcto=False, mensaje=f'Incorrecto. La respuesta correcta era: {pregunta_actual_objeto.respuesta}.')
    return jsonify(correcto=False, mensaje='Ha ocurrido un error.')

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if 'preguntas' not in session or not session['preguntas']:
        # Cargar preguntas desde el archivo CSV y guardar en sesión como diccionarios
        preguntas_totales = cargar_preguntas_desde_csv('econ.csv')
        print(preguntas_totales)
        session['preguntas'] = [pregunta.a_diccionario() for pregunta in preguntas_totales]
        session['preguntas_restantes'] = session['preguntas'].copy()

    if request.method == 'POST':
        if request.form.get('action') == 'Nueva Pregunta':
            if session['preguntas_restantes']:
                # Seleccionar aleatoriamente y eliminar una pregunta del arreglo de preguntas restantes
                indice_pregunta_aleatoria = random.randrange(len(session['preguntas_restantes']))
                pregunta_aleatoria = session['preguntas_restantes'].pop(indice_pregunta_aleatoria)
                # Guardar la pregunta actual en sesión como diccionario
                session['pregunta_actual'] = pregunta_aleatoria
                # Necesitamos hacer un commit de la sesión para asegurarnos de que se guarde la modificación
                session.modified = True
                # Convertir diccionario a objeto Pregunta para pasarlo al template
                pregunta_objeto = Pregunta.desde_diccionario(pregunta_aleatoria)
                return render_template('pregunta.html', pregunta=pregunta_objeto)
            else:
                flash('No hay más preguntas. Reiniciando.', 'info')
                # Reiniciar preguntas restantes desde el arreglo original de preguntas
                session['preguntas_restantes'] = session['preguntas'].copy()
                session.modified = True
        elif request.form.get('action') == 'Enviar Respuesta':
            respuesta_seleccionada = request.form.get('opcion')
            pregunta_actual_diccionario = session.get('pregunta_actual', None)
            if pregunta_actual_diccionario:
                pregunta_actual_objeto = Pregunta.desde_diccionario(pregunta_actual_diccionario)
                # Asegúrate de que la comparación se realiza correctamente
                if respuesta_seleccionada== pregunta_actual_objeto.respuesta:
                    flash('¡Correcto!', 'success')
                else:
                    flash(f'Incorrecto. La respuesta correcta era: {pregunta_actual_objeto.respuesta}', 'danger')

    return render_template('inicio.html')

@app.route('/ver_tablero')
def ver_tablero():
    tablero = session.get('tablero', inicializar_tablero(9, 6))  # Genera un tablero de 8x8
    return render_template('tablero.html', tablero=tablero)
@app.route('/configurar_tablero', methods=['POST'])
def configurar_tablero():
    num_jugadores = request.form.get('num_jugadores', type=int)
    return redirect(url_for('mostrar_tablero', num_jugadores=num_jugadores))

@app.route('/tablero/<int:num_jugadores>')
def mostrar_tablero(num_jugadores):
    # Asegúrate de validar que num_jugadores está en el rango 1-4
    num_jugadores = max(1, min(num_jugadores, 4))
    return render_template('tablero.html', num_jugadores=num_jugadores)

if __name__ == '__main__':
    app.run(debug=True)
