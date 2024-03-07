from flask import Flask, render_template, request, redirect, url_for
import random
from test import *
app = Flask(__name__)

archivo_csv = 'PREGUNTAS.csv'
preguntas = cargar_preguntas_desde_csv(archivo_csv)

@app.route('/', methods=['GET'])
def inicio():

    preguntas_aleatorias =random.sample(preguntas, min(len(preguntas), 5))
    return render_template('index.html', preguntas=preguntas_aleatorias)

@app.route('/verificar', methods=['POST'])
def verificar():
    respuestas_usuario = request.form.to_dict()
    # Aquí iría la lógica para verificar las respuestas del usuario
    # Por simplicidad, redireccionamos al inicio después de enviar respuestas
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
