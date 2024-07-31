import requests
import json

reqUrl = "https://us-central1-aiplatform.googleapis.com/v1/projects/teco-prod-sasbq-bf9d/locations/us-central1/publishers/google/models/code-bison-32k:predict"

headersList = {
    "Authorization": "Bearer ya29.c.c0AY_VpZj3fy25SVkuV-gyWBZmeVfP8OSo3BsVeQTIIVv_PjcY1AhpklZptEAghYvoyDf_z51QgI8Z8IVOPac7-7gCWPFNvTZlkPZBlLJx_TIOnQUAgF18jc0f47-83gFq_QlRX1LzUbOC7yWMYrIY5HvGpIMkX0txc2t3AfbXRS9_HqeHAjv3_mwKQKvcuc9fVpRnSOEYmV3Xgli0Pe5awz8XQCVjQ73OO6RDxTqUo06vb_903bh9KBJT-dV1igu0Wyf9mrCKtfAm4LAoxmCl749wS8QeIDQHl8m1Eghd8nC4SAZY0K8Sl7ZoWWynm88plwy6Zv1fOpzf4Oy7BBimUQjsc4gRFVf73euTaVa6XsC9cuiB73LdWWEqNPk1WOrkuWLQG397PtIfnu22_3aOXioQUg-j6ttBp5aIsX_hXRmyQtbSZt3V2q-_pMY2__9yW2wMwJZZ-UR9q2359ow24ghgMiX3banWSUe6pzRB6u1ZOjw1qFiIleM67RQU7t9u_r42VjrxQ7IueRgXBRq4USInnxbmZj0tMh1IB4ocpo4cF6eoz87rBarZIJ89y3UIqiZWOYlonp_IJ8J6pc5wWaU-2_1zZhZ5IY3FvSSsyJfRsggzq01V4yXp_ZI9WY-WjewnWaSObO9y4nahsQJqXslkQa8I4o5owSzRylae2i9d0xXghoSaFSQUxbWndf27b1uxjyOBw40lzZtWjSJ6h1woudYOq_kqq-2FjbS9FcFm6_m_oj44rFQFqfeksiIcxu0kfY_BkueV-5Sne_tkZsIfYSh18Wtj925S2S7__RMOdtYtrkpci6VUqv0Zopu63f8o1X8SzYcR9anj8J6_aFh8W3F1vSOZaF4w8liVZlfdIaQYq2eu9-Ramt1mXesoxssztB2IJ1vQj2qXx_QYhlMX-I-fjWIujqXJQIbo3F6kiBlatZ1RO-Mjry0j3ReQgyYoukudoiQMUlWBhy9ou933nSSV5xf2Iwus3SpldUpeW5uuxZrj7t3",
    "Content-Type": "application/json",
}

payload = json.dumps(
    {
        "instances": [{"prefix": "print hola mundo en  python"}],
        "parameters": {
            "candidateCount": 1,
            "maxOutputTokens": 8192,
            "temperature": 0.2,
        },
    }
)

response = requests.request("POST", reqUrl, data=payload, headers=headersList)

print(response.text)
