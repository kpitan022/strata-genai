import os
from pprint import pprint
import flet as ft
import logging
from logging.handlers import RotatingFileHandler
from oauth2client.service_account import ServiceAccountCredentials
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel

from login_idp import validar_usuario


path_log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log")
# filehandler = RotatingFileHandler(path_log, maxBytes=100000, backupCount=5)
# filehandler.setLevel(logging.INFO)
# # filehandler.setLevel(logging.ERROR)
# formatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
# )
# logging.basicConfig(
#     level=logging.INFO,
#     # level=logging.ERROR,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler(path_log),
#         logging.StreamHandler(),
#     ],
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
# logging.getLogger("flet_core").setLevel(logging.DEBUG)

# from test_requests import peticion_a_vertex
from new_test_request import peticion_a_vertex

# importo la libre ria para  obtener las variables de entorno
from dotenv import load_dotenv

# traigo las variables de entorno
load_dotenv()

# defino las variables de entorno


# set Flet path to an empty string to serve at the root URL (e.g., https://lizards.ai/)
# or a folder/path to serve beneath the root (e.g., https://lizards.ai/ui/path
DEFAULT_FLET_PATH = ""  # or 'ui/path'
DEFAULT_FLET_PORT = 8502  # or 80


# strata_imagen = "https://strataanalytics.us/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flogo-footer.61fe5313.png&w=640&q=75"
STRATA_IMAGEN = "favicon.png"
CONSEJOS = "docs/consejos.md"


def main(page: ft.Page):
    snack_bar = ft.SnackBar(
        content=ft.Text("El campo de texto no puede estar vacio"),
        # action="Alright!",
        show_close_icon=True,
        action_color=ft.colors.SURFACE_VARIANT,
    )
    page.overlay.append(snack_bar)

    # inicializamos el proyecto de Vertex AI con el nombre teco-playground y la ubicación us-central1
    vertexai.init(project="teco-playground", location="us-central1")

    # instrucciones que se van a utilizar para el modelo generativo de Vertex AI
    TEXT_INSTRUCTION = """vas a tomar un rol de ingniero de datos experto en programación """  # pylint: disable=line-too-long

    # inicializamos el modelo generativo de Vertex AI con el nombre gemini-1.5-flash-001 y el sistema de instrucciones que se va a utilizar
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        # "gemini-1.5-pro-001",
        system_instruction=[TEXT_INSTRUCTION],
    )
    chat = model.start_chat(response_validation=False)

    generation_config = {
        # "max_output_tokens": 8192,
        "temperature": 0.2,
        "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    # función que se encarga de enviar un mensaje a Vertex AI y obtener la respuesta
    def nuevo_mensaje(prompt):
        # sleep(0.5)

        return (
            chat.send_message(
                [prompt],
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            .candidates[0]
            .content.parts[0]
            .text
        )

    # respuestas = []
    respuestas2 = []
    # page.session.set("logeado", False)
    # page.session.set("user", None)
    # simulamos que el usuario  esta logeado en la app
    # page.session.set("logeado", False)
    # page.session.set("user", None)

    # retrocedemos un nivel desde el archivo main.py y luego entramos a la carpeta assets/docs
    path_consejos = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "assets/docs/consejos.md"
    )
    # leemos un archivo markdown y lo guardamos en una variable para renderizarlo en la pagina de inicio
    with open(path_consejos, "r", encoding="utf-8") as f:
        CONSEJOS = f.read()

    def logout_button_click(_):
        # cerramos sesion en la app
        page.session.set("logeado", False)
        page.session.set("user", None)
        page.session.set("iniciales", None)
        # refresco los botones de login y logout
        toggle_login_buttons()
        # redireccionamos y recargamos la pagina
        go_login(_)

    # def on_logout(_):
    #     toggle_login_buttons()

    def toggle_login_buttons():
        logout_button.visible = page.session.get("logeado") is True
        user_name.visible = page.session.get("logeado") is True
        if page.session.get("logeado") and page.session.get("user") is not None:
            user_name.value = page.session.get("user")
            user_name.update()
        avatar.visible = page.session.get("logeado") is True
        if page.session.get("logeado"):
            avatar.foreground_image_url = ft.Icon(
                ft.icons.PERSON_3_SHARP,
                color=ft.colors.BLACK,
            )
            # obtengo las iniciales del nombre del usuario autenticado
            iniciales = "".join(
                [i[0].upper() for i in page.session.get("user").split(" ")]
            )
            page.session.set("iniciales", iniciales)
            # avatar.content = ft.Text(iniciales, color=ft.colors.BLACK)
            avatar.update()

        page.update()

    logout_button = ft.ElevatedButton(
        "Logout", on_click=logout_button_click, icon=ft.icons.LOGOUT_OUTLINED
    )
    user_name = ft.Text(value="")
    avatar = ft.CircleAvatar(
        # foreground_image_url=STRATA_IMAGEN,
        # content=ft.Text("SA"),
        content=ft.Icon(
            ft.icons.PERSON_3_ROUNDED,
        ),
        # bgcolor=ft.colors.SURFACE_VARIANT,
        # color=ft.colors.BLACK,
    )

    toggle_login_buttons()

    page.title = "StrataGenAI"
    page.theme_mode = "dark"
    page.bgcolor = ft.colors.BLACK
    page.window.maximized = True
    page.scroll = "always"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # hacemos que la pagina no pueda ser redimensionada
    page.window.resizable = False

    alto = 1668
    ancho = 670

    page_height = int(alto) * 0.85
    page_width = int(ancho) * 1.5

    main_container = ft.Container(
        content=ft.Text(value="Hola mundo"),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=ft.border_radius.all(5),
        padding=ft.padding.all(10),
        width=page_width,
        # height=(int(alto) * 0.85),
    )

    def containers(altura: int, color: str):
        return ft.Container(
            bgcolor=color,
            border_radius=10,
            height=page_height * (altura / 10),
            # margin=ft.margin.all(5),
            padding=ft.padding.all(5),
        )

    def validar_input(texto: str):
        if texto == "":
            send_button.disabled = True

        else:
            send_button.disabled = False
        send_button.update()

    # crear 3 contenedores para contenido de la pagina uno de cada color y agregarlos a la pagina
    header = containers(1.2, ft.colors.GREY_900)
    sub_header = containers(0.5, ft.colors.GREY_900)
    body = containers(4.1, ft.colors.GREY_900)
    body2 = containers(4.1, ft.colors.GREY_900)
    footer = containers(1, ft.colors.GREY_900)

    # hacemos que body sea un contenedor de tipo columna
    body.content = ft.Column(
        [
            ft.ResponsiveRow(
                [
                    ft.Markdown(
                        value=CONSEJOS,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        on_tap_link=lambda e: page.launch_url(e.data),
                        # extension_set="gitHubWeb",
                        code_theme="atom-one-dark",
                        code_style=ft.TextStyle(font_family="Roboto Mono"),
                    ),
                    # boton para abrir el documento de CONSEJOS en una nueva pestaña
                    ft.IconButton(
                        tooltip="Abrir consejos en una nueva pestaña",
                        icon=ft.icons.OPEN_IN_NEW_OUTLINED,
                        # hacer que el boton descargue el archivo de consejos
                        on_click=lambda _: page.launch_url(
                            "docs/consejos.md",
                            # web_popup_window=True,
                        ),
                    ),
                ]
            ),
        ],
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # height=page_height * (4.1 / 10),
        # width=page_width,
    )

    # hacemos invisible el contenedor body2
    body2.visible = False

    titulo = ft.Text(
        value=" StrataGenAI",
        italic=False,
        selectable=False,
        style=ft.TextThemeStyle.DISPLAY_SMALL,
    )
    subtitulo = ft.Text(
        value="Interfaz de usuario para para la traducción de código fuente utilizando modelos de lenguaje generativos.\nRealizado por el equipo de Strata-Analytics",
        italic=False,
        selectable=False,
        style=ft.TextThemeStyle.BODY_MEDIUM,
    )

    strata_avatar = ft.CircleAvatar(
        foreground_image_url="https://strataanalytics.us/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flogo-footer.61fe5313.png&w=640&q=75",
        # content=ft.Text("SA"),
        bgcolor=ft.colors.WHITE,
        # width=page_width / 15,
    )
    # contenide de el contenedor header
    header.content = ft.Column(
        [
            ft.Row(
                [
                    strata_avatar,
                    titulo,
                    ft.Row(
                        [
                            avatar,
                            user_name,
                            # login_button,
                            logout_button,
                        ],
                        expand=True,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
                # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            subtitulo,
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=page_height / 5,
        width=page_width,
    )

    def reestablecer_chat(_):
        # si body2 es visible entonces hacemos visible body e invisible body2
        if body2.visible:
            body2.visible = False
            body.visible = True
            body2.update()
            body.update()
        # chat.message_history.clear()
        respuestas2.clear()
        # actualizar el contenido de los contenedores
        lv_text.controls.clear()
        lv_md.controls.clear()
        lv_text.update()
        lv_md.update()

    def text_or_md(_):
        lv_text.visible = not lv_text.visible
        lv_md.visible = not lv_md.visible

        lv_text.update()
        lv_md.update()

    btn_reset = ft.IconButton(
        tooltip="Reestablecer chat",
        icon=ft.icons.DELETE_SWEEP_OUTLINED,
        on_click=reestablecer_chat,
    )

    switch_text_md = ft.Switch(
        label="Markdown",
        value=True,
        on_change=text_or_md,
    )

    sub_header.content = ft.Column(
        [
            ft.Row(
                [
                    switch_text_md,
                    btn_reset,
                ],
                expand=True,
                # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        ],
    )

    def on_click_send():
        send_button.visible = not send_button.visible
        loading.visible = not loading.visible
        send_button.update()
        loading.update()

    # lv_text = ft.ListView(
    #     spacing=10,
    #     padding=20,
    #     auto_scroll=True,
    #     visible=False,
    # )
    # lv_md = ft.ListView(
    #     spacing=10,
    #     padding=20,
    #     auto_scroll=True,
    #     # height=300,
    # )
    lv_text = ft.Column(
        visible=False,
    )
    lv_md = ft.Column()

    body2.content = ft.Column(
        [
            lv_text,
            lv_md,
        ],
        expand=True,
        # scroll="always",
        scroll=ft.ScrollMode.ADAPTIVE,
        auto_scroll=True,
    )

    input_text = ft.TextField(
        # value="Ingrese el texto a traducir",
        color=ft.colors.WHITE,
        expand=True,
        hint_text="Ingrese el texto a traducir",
        on_change=validar_input,
        multiline=True,
        # min_lines=1,
        max_length=25000,
        shift_enter=True,
        on_submit=lambda e: send_button.on_click(e),
    )

    def agregar_item2():
        # si body es visible entonces agregamos el texto a body2 y hacemos visible body2 e invisible body
        if body.visible:
            body.visible = False
            body2.visible = True
            body2.update()
            body.update()

        lv_text.controls.append(
            ft.Column(
                controls=[
                    ft.Container(
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.CircleAvatar(
                                            # foreground_image_url="https://www.telecom.com.ar/web/favicon.ico",
                                            # max_radius=20,
                                            content=ft.Text(
                                                page.session.get("iniciales")
                                            ),
                                        ),
                                        ft.Text(value=user_name.value),
                                    ]
                                ),
                                ft.Text(
                                    value=respuestas2[-2]["content"],
                                    # value=texto,
                                    selectable=True,
                                    # bgcolor=ft.colors.SURFACE_VARIANT,
                                ),
                            ],
                        ),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=10,
                        padding=ft.padding.all(5),
                    ),
                    ft.Container(
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.CircleAvatar(
                                            foreground_image_url=STRATA_IMAGEN,
                                            # max_radius=20,
                                            # content=ft.Text("SA"),
                                            bgcolor=ft.colors.WHITE,
                                        ),
                                        ft.Text(value="StrataGenAI:"),
                                    ]
                                ),
                                ft.Text(
                                    value=respuestas2[-1]["content"],
                                    # value=resultado,
                                    selectable=True,
                                ),
                            ],
                        ),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=10,
                        padding=ft.padding.all(5),
                    ),
                    ft.Divider(),
                ]
            )
        )
        lv_md.controls.append(
            ft.Column(
                controls=[
                    ft.Container(
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.CircleAvatar(
                                            # foreground_image_url="https://www.telecom.com.ar/web/favicon.ico",
                                            # max_radius=20,
                                            content=ft.Text(
                                                page.session.get("iniciales")
                                            ),
                                        ),
                                        ft.Text(value=user_name.value),
                                    ]
                                ),
                                ft.Text(
                                    value=respuestas2[-2]["content"],
                                    # value=texto,
                                    selectable=True,
                                    # bgcolor=ft.colors.SURFACE_VARIANT,
                                ),
                            ],
                        ),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=10,
                        padding=ft.padding.all(5),
                    ),
                    ft.Container(
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.CircleAvatar(
                                            foreground_image_url=STRATA_IMAGEN,
                                            # max_radius=20,
                                            # content=ft.Text("SA"),
                                            bgcolor=ft.colors.WHITE,
                                        ),
                                        ft.Text(value="StrataGenAI:"),
                                    ]
                                ),
                                ft.Markdown(
                                    value=respuestas2[-1]["content"],
                                    # value=resultado,
                                    selectable=True,
                                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                    on_tap_link=lambda e: page.launch_url(e.data),
                                    # extension_set="gitHubWeb",
                                    code_theme="atom-one-dark",
                                    code_style=ft.TextStyle(font_family="Roboto Mono"),
                                ),
                            ],
                        ),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=10,
                        padding=ft.padding.all(5),
                    ),
                    ft.Divider(),
                ]
            )
        )
        lv_text.update()
        lv_md.update()

    def traducir(texto):
        if len(texto) != 0:
            on_click_send()
            input_text.disabled = True if page.auth is not None else False
            input_text.update()
            send_button.disabled = True
            send_button.update()
            if page.session.get("logeado") is False:
                # body_text.value = "Debe iniciar sesión para poder traducir"
                # body_text.update()
                # body_md.value = "Debe iniciar sesión para poder traducir"
                # body_md.update()
                on_click_send()
                return "Debe iniciar sesión para poder traducir"
            # user_token = page.auth.token.access_token
            # user_token = page.auth.token.refresh_token

            # body_text.update()
            respuestas2.append({"author": page.session.get("user"), "content": texto})
            reschat = nuevo_mensaje(texto)
            # resultado = peticion_a_vertex(
            #     # page.auth.token.access_token,
            #     respuestas2,
            # )
            # respuestas2.append({"author": "StrataGenAI", "content": resultado})
            respuestas2.append({"author": "StrataGenAI", "content": reschat})
            # body_text.value = resultado
            # body_text.update()
            # add_text_list(texto, resultado)
            # agregar_item(texto, resultado)
            # add_dict_to_list(texto)
            agregar_item2()
            input_text.value = ""
            input_text.disabled = False
            input_text.update()
            on_click_send()
            # return texto
        else:
            # Lanzamos un mensaje de error si el campo de texto esta vacio

            snack_bar.open = True
            snack_bar.update()

    send_button = ft.IconButton(
        icon="send",
        disabled=True,
        # tooltip=
        on_click=lambda _: traducir(input_text.value),
    )

    loading = ft.ProgressRing(
        color=ft.colors.SURFACE_VARIANT,
        visible=False,
        stroke_width=5,
    )

    # contenido del contenedor footer un cuadro ingreso de texto y un boton para enviar la petición
    footer.content = ft.Row(
        [
            # login_button,
            # logout_button,
            # user_name,
            input_text,
            send_button,
            loading,
        ],
        expand=True,
        # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=page_height / 5,
        width=page_width,
    )

    main_container.content = ft.Column(
        [
            header,
            sub_header,
            # switch_text_md,
            body,
            body2,
            footer,
        ]
    )

    home = ft.SafeArea(
        main_container,
        # expand=True,
    )
    error_login = ft.Text(
        value="",
        color=ft.colors.RED,
        visible=False,
    )

    def go_home(_):
        page.route = "/"
        page.clean()
        page.add(home)
        page.update()

    def go_login(_):
        page.route = "/login"
        page.clean()
        page.add(
            ft.SafeArea(
                main_login,
                # expand=True,
            ),
        )

        page.route = "/login"
        page.update()

    # def redireccion(e):
    #     if page.route == "/login":
    #         page.route = "/"
    #         page.clean()
    #         page.add(home)
    #         page.update()
    #     else:
    #         page.route = "/login"
    #         page.update()

    def proceso_login(_):
        # validamos que el usuario tenga acceso a la app
        req, nombre = validar_usuario(username.value, password.value)
        if req:
            # si el usuario tiene acceso a la app entonces lo redireccionamos a la pagina de inicio
            page.route = "/"
            page.clean()
            page.add(home)
            # cambiamos el valor de la variable de sesion logeado a True para indicar que el usuario esta logeado en la app
            page.session.set("logeado", True)
            # cambiamos el valor de la variable de sesion user por el usuario autenticado
            page.session.set("user", nombre)
            page.update()
            toggle_login_buttons()
        else:
            # si el usuario no tiene acceso a la app entonces mostramos un mensaje de error
            error_login.visible = True
            error_login.value = nombre
            error_login.update()

    def mostrar_contrasena(e):
        password.password = not password.password
        password.update()

    # funcion para validar que los campos de usuario y contraseña no esten vacios y habilitar el boton de login
    def validar_login(e):
        if username.value == "" or password.value == "":
            login_btn.disabled = True
            # mostrar el mensaje de error en caso de que este visible
            error_login.value = (
                "Los campos de usuario y contraseña no pueden estar vacios"
            )
            error_login.visible = True
            error_login.update()
        else:
            login_btn.disabled = False
            # ocultar el mensaje de error en caso de que este visible
            error_login.visible = False
            error_login.value = ""
            error_login.update()

        login_btn.update()

    mostrar_password = ft.Switch(
        label="Mostrar contraseña",
        value=False,
        on_change=mostrar_contrasena,
    )

    mostrar_password_row = ft.Row(
        [
            mostrar_password,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    username = ft.TextField(
        label="Ingrese su usuario U",
        bgcolor=ft.colors.GREY_900,
        icon=ft.icons.EMAIL_OUTLINED,
        on_change=validar_login,
    )
    text_username = ft.Row(
        [
            username,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    password = ft.TextField(
        label="Ingrese su contraseña",
        password=True,
        bgcolor=ft.colors.GREY_900,
        icon=ft.icons.LOCK_OUTLINED,
        on_change=validar_login,
    )

    password_row = ft.Row(
        [
            password,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    main_login = ft.Container(
        content=ft.Text(value="Hola mundo"),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.GREY_900,
        border_radius=ft.border_radius.all(5),
        padding=ft.padding.all(10),
        width=page_width,
        # height=page_height,
        expand=True,
    )

    body_login = ft.Container(
        content=ft.Text(value="Hola mundo"),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=ft.border_radius.all(5),
        padding=ft.padding.all(50),
        # width 1/3 del ancho de la pagina
        # width=page_width / 3,
        # width=page_width,
        # height=(int(alto) * 0.85),
    )

    body_login.content = ft.Column(
        [
            text_username,
            password_row,
            mostrar_password_row,
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        # height=page_height / 5,
        # width=page_width,
    )

    login_btn = ft.ElevatedButton(
        "Login",
        # on_click=go_home,
        on_click=proceso_login,
        icon=ft.icons.LOGIN_OUTLINED,
        disabled=True,
    )

    main_login.content = ft.Column(
        [
            header,
            body_login,
            login_btn,
            error_login,
        ],
        # expand=False,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # simulamos que el usuario  esta logeado en la app
    page.session.set("logeado", True)
    page.session.set("user", "Usuario de prueba")

    if page.session.get("logeado"):
        page.add(
            home,
        )
        page.route = "/"
    else:
        page.add(
            ft.SafeArea(
                main_login,
                # expand=True,
            ),
        )
        page.route = "/login"

    # page.add(
    #     home,
    # )


# ft.app(
#     target=main,
#     port=PORT,
#     view=ft.WEB_BROWSER,
#     route_url_strategy="path",
# )

# if __name__ == "__main__":
#     flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
#     # flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
#     ft.app(
#         name=flet_path,
#         target=main,
#         view=None,
#         # view=ft.WEB_BROWSER,
#         # port=flet_port,
#         route_url_strategy="path",
#         use_color_emoji=True,
#         web_renderer=ft.WebRenderer.CANVAS_KIT,
#         assets_dir="assets",
#     )
ft.app(
    name="StrataGenAI",
    target=main,
    # view=None,
    view=ft.AppView.FLET_APP,
    # port=flet_port,
    route_url_strategy="path",
    use_color_emoji=True,
    web_renderer=ft.WebRenderer.CANVAS_KIT,
    assets_dir="assets",
)
