import time
import schedule
import os
import telebot # Importamos las librería
#from http.client import httplib
#from urllib.parse import urlparse, parse_qs
import requests
from lxml import html
from bs4 import BeautifulSoup

TOKEN=os.environ.get("TOKEN") # Ponemos nuestro Token generado con el @BotFather
bot = telebot.TeleBot(TOKEN)  #Creamos nuestra instancia "bot" a partir de ese TOKEN
idGrupoFrom = os.environ.get("IDMIGRA")

user = bot.get_me()
#print(user)
#Es equivalente a esto 
#https://api.telegram.org/bot<TU_TOKEN>/getMe

# Saber información de los grupos del Bot
updates = bot.get_updates()
#print(updates)
#Es equivalente a esto 
#https://api.telegram.org/bot<TU_TOKEN/getUpdates

def enviarMensaje(mensaje):
    requests.post('https://api.telegram.org/bot' + TOKEN + '/sendMessage', data={'chat_id': idGrupo, 'text': mensaje, 'parse_mode': 'HTML'})
    
def enviarDocumento(ruta):
    requests.post('https://api.telegram.org/bot' + idBot + '/sendDocument',
              files={'document': (ruta, open(ruta, 'rb'))},
              data={'chat_id': idGrupoFrom, 'caption': 'imagen caption'})
    
#Grupo del SAREN/SAIME
chat_id = os.environ.get("CHAT_ID")
#bot.send_message(chat_id, "Mensaje automático de prueba") ##envío del mensaje
print(chat_id)

###################################################################
web='http://citas.saren.gob.ve/citas/create?id=2'
web_login="http://citas.saren.gob.ve/login"

# funcion que se encarga de obtener respuesta del estatus del servidor web
def get_server_status_code(url):
    # descarga sólo el encabezado de una URL y devolver el código de estado del servidor.
    host, path = urlparse.urlparse(url)[1:3]
    try:
        conexion = httplib.HTTPConnection(host)
        conexion.request('HEAD', path)
        return conexion.getresponse().status
    except StandardError:
        return None

# función que se encarga de checkear que exista la url a guardar
def check_url(url):
    # Comprobar si existe un URL sin necesidad de descargar todo el archivo. Sólo comprobar el encabezado URL.
    # variable que se encarga de traer las respuestas
    codigo = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in codigo

#print(check_url(web))
#x = requests.get(web)
#print(x) #x devuelve el estado de la respuesta y x.text el formato del documento

################################################################
### 1 Variables a utilizar
##archivo = open("file1.txt","r") 
##USERNAME = os.environ.get("USERNAME")
##PASSWORD = os.environ.get("PASSWORD")
##LOGIN_URL = "http://citas.saren.gob.ve/login"
##URL = 'http://citas.saren.gob.ve/citas/create?id=2'
##URL_API='https://www.google.com/recaptcha/api2/reload?k=6LcITUQUAAAAAOz2ujShu968RHhwEASY9gdC6Ot-'
##def main():
##    # 2 Get login 
##    session_requests = requests.session()
##    result = session_requests.get(LOGIN_URL)
##
##    # 3 Create payload
##    payload = {
##        "_token":"OZIXdehYVSQqoIBFos0E6hOiuPgKIx9U6TgyxMsN",
##        "email": USERNAME, 
##        "password": PASSWORD, 
##        }
##
##    # 4 Perform login
##    response = requests.post(LOGIN_URL, data=payload, proxies=proxies)
##    estado = response.status_code
##    #session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
##
##    # 5 Scrape url
##    #result = session_requests.get(URL, headers = dict(referer = URL))
##    #print(result)
##    #tree = html.fromstring(result.content)
##    #x = requests.get(url)
##    #print(x.text)
##    ##query=tree.xpath("//tr[@class='menu' or @class='img img-responsive sinfecha']/td[position()=2]/text()")
##    #enquiries = tree.xpath("//tr[@class='menu' or @class='img img-responsive sinfecha']")
##
##    #for enquirie in enquiries:
##        #print(enquirie)
##
##    if estado == 200:
##        try:
##            '''
##                    Analizar resultado en base a su html
##            '''
##            contenido = response.content
##            soup = BeautifulSoup(contenido,"lxml")
##
##            #Aqui depende del contenido del html que respondan (este sera como ejemplo)
##
##            #Obtiene la parte del codigo html donde el id="mensaje-respuesta"
##            #tambien pueden cambiarle a "class":"tipo-clase"
##            datos = soup.find_all(True, {"id":"mensaje-respuesta"})
##
##            #De la lista obtenido, tomamos los elementos
##            for tag in datos:
##                for linea in tag:
##                    linea = linea.strip()
##
##                    #Ejemplo de analisis de resultados
##                    if linea=="Cuenta correcta":
##                        print("User:"+USERNAME+" + Clave:"+PASSWORD+" -> Login aceptado!")
##
##                    elif linea=="Contraseña incorrecta":
##                        print( "User:"+USERNAME+" + Clave:"+PASSWORD+" -> Contraseña incorrecta")
##
##                    else:
##                        print( "User:"+USERNAME+" + Clave:"+PASSWORD+" -> "+linea)
##        except:
##            print( "Except:"+USERNAME+":"+PASSWORD+"\n"	)
##
##    else:
##        print( "Error: "+str(estado)+"-> " +USERNAME+":"+PASSWORD+"\n")
##	
##    #Cerrar archivo
##    archivo.close()
##
##main()
