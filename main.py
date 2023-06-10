'''
PENDING
- Definir una forma de navegar los productos de meli
- Evaluar todas las reviews (buscar como no repetir evaluaciones y guardarlas)
- Cuando le pega a discord deberia mandar el item y reseña evaluadas
'''



import os
import openai
import json
from discord_webhook import DiscordWebhook

SYSTEM_MSG = 'Sos una IA encargada de curar el contenido para una cuenta de twitter de reseñas graciosas en mercadolibre. Cada vez que te envie una reseña vas a devolver con un json que diga, que tan graciosa es del 1 al 100 y la razon. Por ejemplo:\
{\
  "graciosa": 80,\
  "motivo": "porque asi no es como se usa el producto"\
}\
Solo vas a contestar exclusivamente en ese formato.'

USER_MSG = 'Producto: Brother HL1212W Impresora Láser Wi-Fi color Negro/Blanco 220V\
Reseña: Es una impresora de batalla, no le pidas lujos ni nada, le doy 5 estrellas porque es justo lo que estaba buscando. Es muy buena impresora, practica y básica! en cuanto a calidad los plásticos son duros y correctos para el precio. El software para la pc es solo para usarlo de driver no le pidas muchas configuraciones extra. Calidad de impresión muy buena. Muy importante y lo mejor los cartuchos de tóner son baratos, no tienen chip, y rinden (hasta se pueden recargar). En mi caso no me funciono directo con airprint pero con la aplicación brother iprint&scan funciona perfecto, imprimí documentos e imágenes desde el celular sin problema (todo en byn obvio). Es media lenta para iniciar a imprimir pero es comprensible xq la tengo conectada por wifi. Para el uso normar de estudio y trabajo que le doy esta mas que perfecto.'

def get_response(user_msg, system_msg):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )

    return response

try:
    openai.api_key = os.getenv("OPENAI")

    response = get_response(USER_MSG, SYSTEM_MSG)

    print("Finish reason:", response["choices"][0]["finish_reason"])

    model_message = response["choices"][0]["message"]["content"]
    print("Model's message:", model_message)

    try:
        message_json = json.loads(model_message)
    except json.JSONDecodeError as e:
        print("El mensaje del modelo no es un JSON válido. Detalles: ", e)
        message_json = {}

    if 'graciosa' in message_json and message_json['graciosa'] > 2:
        url = 'https://discord.com/api/webhooks/1117068798965588030/k4GwfMUwHnWJSnbpoDmsG58GyuAlgAkZjSaVr3nCL95jMZNJ05ky4Ee74MmjPUy764hj'
        webhook = DiscordWebhook(url=url, content=json.dumps(message_json))
        webhook.execute()

except KeyError:
    print("Por favor, establece la variable de entorno OPENAI.")
