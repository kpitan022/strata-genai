import requests
import dotenv
import json
import os

dotenv.load_dotenv()


def get_token():
    CLIENT_ID = os.getenv("CLIENT_ID_IDP")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET_IDP")

    reqUrl = "https://iamrest.telecom.com.ar:8443/api/v2/token"

    headersList = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "description": "GCP-STRATA_GEN",
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload, headers=headersList)

    token = json.loads(response.text)["access_token"]
    return token


def validar_usuario(user, password):
    return True, "Demo User"
    reqUrl = "https://iamrest.telecom.com.ar:8443/api/v2/users/tuid/auth"

    headersList = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }

    payload = {"user": user, "password": password}

    response = requests.request(
        "POST", reqUrl, data=json.dumps(payload), headers=headersList
    )

    data = json.loads(response.text)
    # el contenido de la respuesta es similar a:
    # {
    #     "status": "Success",
    #     "success": true,
    #     "message": "Login successful",
    #     "totalSize": 6,
    #     "records": {
    #         "user": [
    #         {
    #             "dn": "cn=u935654,ou=Personas,ou=Usuarios,o=Telecom",
    #             "uid": "u935654",
    #             "fullname": "Franco Paolo Rossi",
    #             "givenname": "Franco Paolo",
    #             "sn": "Rossi",
    #             "mail": "FPROSSI@PROVEEDOR.TECO.COM.AR"
    #         }
    #         ],
    #         "roles": [
    #         {
    #             "dn": "cn=20230706160300255,cn=DATAOFFICE_CDP,cn=GCP,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=UserApplication,cn=DriverSet1,ou=Servicios,o=Telecom",
    #             "tvalue": "GAPP_DATAOFFICE_CDP_GCP_PROD",
    #             "tname": "GAPP_DATAOFFICE_CDP_GCP_PROD",
    #             "tsystemname": "GCP",
    #             "tapplicationname": "DATAOFFICE_CDP"
    #         },
    #         {
    #             "dn": "cn=20220914114524524,cn=BQ_DATALAKE_DIGITAL_YOIZEN,cn=GCP,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=UserApplication,cn=DriverSet1,ou=Servicios,o=Telecom",
    #             "tvalue": "GAPP_GCP_BQ_DATALAKE_DIGITAL_YOIZEN",
    #             "tname": "Digital Yoizen viewer",
    #             "tsystemname": "GCP",
    #             "tapplicationname": "BQ_DATALAKE_DIGITAL_YOIZEN"
    #         },
    #         {
    #             "dn": "cn=20220826102044568,cn=BQ_DATALAKE_EDW_SALESFORCE,cn=GCP,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=UserApplication,cn=DriverSet1,ou=Servicios,o=Telecom",
    #             "tvalue": "GAPP_GCP_BQ_DATALAKE_EDW_SALESFORCE",
    #             "tname": "SALESFORCE viewer",
    #             "tsystemname": "GCP",
    #             "tapplicationname": "BQ_DATALAKE_EDW_SALESFORCE"
    #         },
    #         {
    #             "dn": "cn=20220505141115270,cn=BQ_DATALAKE_GA360,cn=GCP,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=UserApplication,cn=DriverSet1,ou=Servicios,o=Telecom",
    #             "tvalue": "GAPP_GCP_BQ_DATALAKE_GA360",
    #             "tname": "GA360 viewer",
    #             "tsystemname": "GCP",
    #             "tapplicationname": "BQ_DATALAKE_GA360"
    #         },
    #         {
    #             "dn": "cn=20220405121919546,cn=DATAOFFICE_CDP,cn=GCP,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=UserApplication,cn=DriverSet1,ou=Servicios,o=Telecom",
    #             "tvalue": "GAPP_DATAOFFICE_CDP_GCP_DEVS",
    #             "tname": "GAPP_DATAOFFICE_CDP_GCP_DEVS",
    #             "tsystemname": "GCP",
    #             "tapplicationname": "DATAOFFICE_CDP"
    #         }
    #         ],
    #         "status": true
    #     }
    #     }

    # valido que la respuesta sea "success": true
    CLAVE = "STRATA GEN"
    # CLAVE = "DATAOFFICE_CDP"
    validado = False
    if data["success"]:
        return True, data["records"]["user"][0]["fullname"]
        # valido que el usuario tenga tappplicationname = "STRATA GEN"
        roles = data["records"]["roles"]
        for rol in roles:
            if rol["tapplicationname"] == CLAVE:
                validado = True
                break
        if not validado:
            return (
                False,
                "Solicite acceso a la App STRATA GEN a través de la plataforma de gestión de accesos de Telecom",
            )

        return True, data["records"]["user"][0]["fullname"]
    else:
        return (
            False,
            "Ingrese un usuario y contraseña validos y que tenga acceso a la App STRATA GEN",
        )


if __name__ == "__main__":
    # validar_usuario("935654", "PY6mx_)6U")
    print(validar_usuario("u935654", "PY6mx_)6U"))
