import json
from pprint import pprint
import requests

API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
PROJECT_ID = "teco-playground"
MODEL_ID = "codechat-bison-32k"


def peticion_a_vertex(token: str, mensajes: list):
    """
    Función que realiza una petición a Vertex AI
    :param consulta: Consulta a realizar
    :param token: Token de acceso (obtenido con $gcloud auth print-access-token)
    :return: Respuesta de Vertex AI
    """
    headers = {
        "Authorization": f"Bearer {token}",
    }

    payload = json.dumps(
        {
            "instances": [{"messages": mensajes}],
            "parameters": {
                # "candidateCount": 1,
                "maxOutputTokens": 8192,
                "temperature": 0.2,
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

    # pprint(repuesta)
    return repuesta


if __name__ == "__main__":
    tk = "AIzaSyCbRXM6ZaUVmSnWNvk--233-h4Sd9PYmdk"
    respuesta = peticion_a_vertex(tk, ["hola"])
    pprint(respuesta)
