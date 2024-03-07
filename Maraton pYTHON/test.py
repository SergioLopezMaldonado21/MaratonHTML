import pandas as pd
import random
class Pregunta:
    def __init__(self, pregunta, opciones, respuesta):
        self.texto = pregunta
        self.opciones = opciones
        self.respuesta = respuesta

    def __repr__(self):  # Opcional, útil para depuración
        return f"Pregunta(pregunta={self.pregunta}, opciones={self.opciones}, respuesta={self.respuesta})"

def cargar_preguntas_desde_csv(archivo):
    preguntas = []
    df = pd.read_csv(archivo)
    df = df.dropna(subset=['preguntas'])  # Eliminar filas con valores NaN en la columna 'preguntas'
    for index, row in df.iterrows():
        pregunta = Pregunta(row['preguntas'], str(row['opciones']).strip('][').split(', '), row['respuesta'])
        preguntas.append(pregunta)
    return preguntas

def jugar_pregunta(preguntas_disponibles):
    pregunta_seleccionada = random.choice(preguntas_disponibles)
    print("\n" + pregunta_seleccionada.texto)
    for opcion in pregunta_seleccionada.opciones:
        print(opcion)

    respuesta_usuario = input("¿Cuál es tu respuesta? (A, B, C, D): ").strip().upper()
    while respuesta_usuario not in ["A", "B", "C", "D"]:
        print("Respuesta inválida. Por favor, introduce A, B, C, o D.")
        respuesta_usuario = input("¿Cuál es tu respuesta? (A, B, C, D): ").strip().upper()

    if respuesta_usuario == pregunta_seleccionada.respuesta:
        print("¡Correcto! Has acertado la pregunta.")
    else:
        print(f"Incorrecto. La respuesta correcta era la {pregunta_seleccionada.respuesta}.")

    preguntas_disponibles.remove(pregunta_seleccionada)

def main():
    archivo_csv = 'PREGUNTAS.csv'  # Asegúrate de tener este archivo en el formato correcto
    preguntas_originales = cargar_preguntas_desde_csv(archivo_csv)
    preguntas_para_jugar = preguntas_originales.copy()

    seguir_jugando = True
    while seguir_jugando:
        if not preguntas_para_jugar:  # Si no hay más preguntas disponibles, reiniciar la lista
            print("\nHas respondido todas las preguntas. Vamos a reiniciar.")
            preguntas_para_jugar = preguntas_originales.copy()

        jugar_pregunta(preguntas_para_jugar)

        respuesta_jugar_de_nuevo = input("\n¿Quieres seguir jugando? (S o N): ").strip().upper()
        if respuesta_jugar_de_nuevo != "S":
            seguir_jugando = False

    print("Gracias por jugar. Espero que hayas aprendido algo nuevo.")

if __name__ == "__main__":
    main()