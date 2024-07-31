import json
import subprocess
from pprint import pprint

import requests

# API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
PROJECT_ID = "teco-playground"
MODEL_ID = "codechat-bison-32k"

API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
# PROJECT_ID = "teco-prod-sasbq-bf9d"
# MODEL_ID = "codechat-bison"
LOCATION_ID = "us-central1"


def get_token():
    # Intento obtener desde la consola de GCP el token de acceso
    # $gcloud auth print-access-token
    # en caso de que no funcione, se puede obtener desde la consola de GCP
    # en la sección de credenciales

    try:
        token = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            capture_output=True,
            text=True,
        ).stdout.strip()
    except FileNotFoundError:
        token = ""
    return token
    # token = subprocess.run(
    #     ["gcloud", "auth", "print-access-token"],
    #     capture_output=True,
    #     text=True,
    # ).stdout.strip()
    # print(token)
    return token
    return "ya29.c.c0AY_VpZi_YP8u6QJusHnYaHK31BEHVQC_ryXGWqQADj_AoOtQm6EGWIkcmm9OSYpaqTbosvGP6QSnLO5vGJcpnWCUtT433zlQXkwdZRK7VjjG78INBsgl1sFbUAB3Y7RXDzSQqE6hrLh64CEXJAtX8rzzStsqw2EifKs7J9sNR3OOTYTh6N2QjCYpjjlHpbr64OoTfrZrVXyQfMDU5BoJY9NnS1aQExoHb2AhIBKnQL5SXPjRNkxG2DbzXlw8ozdT4eDRYXDR5tREE0YeCTsGH3ibAO9huJbxslY1YLzSzm0rn3LdrftbQwfrk4QfmV-p_CLvDUBrvml1GnzrOdZz7wJn1emu47N3FKRR13gS1ryP_AG_yl1IVvKErS1kSdxsu3lZG397AF2i5uWIna96kgmJ3q-wFvByQoo2FnFVi3eat3j_sh54ecIBlfmgmggOq0a5a-y1riYymeFuB2tmhqmlRmtSbwF59nWe4WaBl2sR9I5u9-xevZWy6_ohRhYBURU11u8fRIB-pqFMijIM58Ubx0pof49xg11csiRp-02g9zq07JBwnz8rYo8jBo1JfkRXxVe18qfbgkyB3_3l3kJ4QtWeo-RZjQ1lJ3wVIp8IWaVsiW2Vy-bnVpjFzhUattXitZcZZtyJ4Uaq_RR1j_9yr9BdZI4ibVUnm4SZedutg9budI1fW0sRBUgYovfQ7WcZWxvXj_va3npS_4tatZsRiQZUQhr8VbwFFopvxc0dcUg61vWuSXvU1z9YX24dOVuwSgqqZI2xUzui8srmZ2mO2Vhy40-320MqSlu6y9b2oBjpkJhJOl3ctmZJaklkSj9gxdWXwVm9-52ceYisR9yIiFafRky23gMmIR38rf_yympe4QOmu0rZm53mykwMn-XsIt2ai004p8BUjbgFh8_i7BnpB3oZcYbu8j67dyd0hcuy_9RiJVRwMldgIm7qx1R905VhqphRhmrF9F21vZ0sFZ9dZoemoI6iMvYIyg4SS50rR_XI7IO"


def peticion_a_vertex(mensajes: list):
    """
    Función que realiza una petición a Vertex AI
    :param consulta: Consulta a realizar
    :param token: Token de acceso (obtenido con $gcloud auth print-access-token)
    :return: Respuesta de Vertex AI
    """
    headers = {
        "Authorization": f"Bearer {get_token()}",
    }

    payload = json.dumps(
        {
            "instances": [{"messages": mensajes}],
            "parameters": {
                # "candidateCount": 1,
                "maxOutputTokens": 8192,
                "temperature": 0.3,
            },
        }
    )
    response = requests.post(
        f"https://{API_ENDPOINT}/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/{MODEL_ID}:predict",
        headers=headers,
        data=payload,
    )
    try:
        # repuesta = response.json()["predictions"][0]["content"]
        repuesta = response.json()["predictions"][0]["candidates"][0]["content"]
    except KeyError:
        repuesta = response.json()["error"]["message"]

    # repuesta = response.json()["predictions"][0]["content"]

    pprint(repuesta)
    return repuesta


if __name__ == "__main__":
    respuesta = peticion_a_vertex(
        [{"author": "StrataGenAI", "content": "imprime hola mundo en python"}]
    )
    # imprimir la respuesta
    pprint(respuesta)
