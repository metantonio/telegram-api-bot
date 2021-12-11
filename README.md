# Localizar número celular (no de manera exacta, la API es pública)
<!-- Sección portada del repositorio -->
<a href="#">
    <img src="./portada.jpg" />
</a>
Este script en python se realizó para crear un BOT.

# TELEGRAM
Lo que primero que tienes que hacer es mandar un mensaje desde Telegram al BotFather (@BotFather), en concreto el de «/newbot».

Posteriormente el propio bot te preguntará por el nombre que quieres para tu bot. Importante, tiene que terminar en la palabra Bot. Ejemplo: SuperBot o super_Bot.

Si todo está correcto, te verificará la creación de tu Bot.

Bot creado y listo para personalizar. El BotFather no asignara un TOKEN o código único de nuestro Bot para poder usarlo más adelante.

Es opcional configurar la privacidad de tu bot, pero es recomendable. Escribimos «/setprivacy» y posteriormente, el nombre de tu bot mencionándolo por su nombre «@Bot». El BotFather te responderá con las opciones que puedes configurar, por ejemplo que cualquiera lo pueda usar o que responda solo a determinados grupos o usuarios.

Descargar los archivos en una misma carpeta.

## Qué se necesita si soy usuario de Windows?

Se necesita tener instalado Python 3.9 (preferiblemente), el cual puede descargarse desde la tienda oficial de Microsoft de forma gratuita.

- [Python 3.9](https://www.microsoft.com/store/productId/9P7QFQMJRFP7)


También es necesario instalar algunas dependencias de Python la primera vez para el correcto funcionamiento del script, para esto tan sólo se debe dar doble click al archivo: `instalar dependencias.bat`. Si por el contrario, se desean instalar las dependencias de Python de forma manual, es necesario ejecutar las siguientes líneas de código en el prompt (parece repetir, pero es una forma de evitar errores si hay más de una versión de python en el pc, o más de un usuario incluso en windows):

```sh
pipenv install
pipenv install pyTelegramBotAPI
```

## Cómo ejecuto el script de Python?

Crear un archivo .env:

```sh
cp .env.example .env
```

Para ejecutar el script, se debe ejecutar un ambiente virtual, hay que abrir el prompt de Windows, navegar hasta la dirección en que están contenidos los archivos, y ejecutar:

```sh
pipenv shell
pipenv run main.py
```

O ejecutar el archivo `pipenv shell.bat` y luego de abierta la consola, colocar:

```sh
pipenv run main.py
```
