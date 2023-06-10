import os
import openai

# Definir los mensajes
SYSTEM_MSG = 'Sos una IA encargada de curar el contenido para una cuenta de twitter de reseñas graciosas en mercadolibre. Cada vez que te envie una reseña vas a devolver con un json que diga, que tan graciosa es del 1 al 100 y la razon. Por ejemplo:\
{\
  "graciosa": 80,\
  "motivo": "porque asi no es como se usa el producto"\
}\
Solo vas a contestar exclusivamente en ese formato.'

USER_MSG = 'Producto: Brother HL1212W Impresora Láser Wi-Fi color Negro/Blanco 220V\
Reseña: Es una impresora de batalla, no le pidas lujos ni nada, le doy 5 estrellas porque es justo lo que estaba buscando. Es muy buena impresora, practica y básica! en cuanto a calidad los plásticos son duros y correctos para el precio. El software para la pc es solo para usarlo de driver no le pidas muchas configuraciones extra. Calidad de impresión muy buena. Muy importante y lo mejor los cartuchos de tóner son baratos, no tienen chip, y rinden (hasta se pueden recargar). En mi caso no me funciono directo con airprint pero con la aplicación brother iprint&scan funciona perfecto, imprimí documentos e imágenes desde el celular sin problema (todo en byn obvio). Es media lenta para iniciar a imprimir pero es comprensible xq la tengo conectada por wifi. Para el uso normar de estudio y trabajo que le doy esta mas que perfecto.'

def get_response(user_msg, system_msg):
    # Llamada a la API de OpenAI con el modelo GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Sustituir por "gpt-4" cuando esté disponible
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )

    return response

try:
    # Configurar la clave de la API de OpenAI
    openai.api_key = os.environ["OPENAI"]

    # Obtener respuesta
    response = get_response(USER_MSG, SYSTEM_MSG)

    # Comprobar el motivo por el que el modelo dejó de generar más salida
    print("Finish reason:", response["choices"][0]["finish_reason"])

    # Extraer el mensaje del modelo de la respuesta
    print("Model's message:", response["choices"][0]["message"]["content"])

except KeyError:
    print("Por favor, establece la variable de entorno OPENAI.")
