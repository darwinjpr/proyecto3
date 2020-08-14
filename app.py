
import time
import tkinter as tk
import subprocess #para ejecutar en terminal de computador
import paramiko #para ejecutar remoto
#from getpass import getpass

class Application(tk.Frame):
	def __init__(self, master=None):#crea la raiz o ventana principal de la app
		super().__init__(master)
		self.master = master
		self.master.geometry("800x600")
		self.master.resizable(0,0)
		self.master.title("aplicacion de seguridad")
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		#crea las partes de la app

		self.etiq_user = tk.Label(self, text="Usuario:", font="Arial")
		self.usuario = str
		self.ctext_user = tk.Entry(self, textvariable=self.usuario,width=30)

		self.etiq_clave = tk.Label(self, text="Contraseña:", font="Arial")
		self.clave = str 
		self.ctext_clave = tk.Entry(self, textvariable=self.clave, show="*", width=30)

		self.etiq_ip = tk.Label(self, text="Direccion IP:", font="Arial")
		self.ip = str   
		self.ctext_ip = tk.Entry(self, textvariable=self.ip,width=30)	

		self.connect_ssh = tk.Button(self)
		self.connect_ssh["text"] = "Comprobar datos de conexion."
		self.connect_ssh["command"] = self.connect

		self.quit = tk.Button(self, text="SALIR", fg="red")
		self.quit["command"] = self.exit

		#Acomoda partes de la app en la ventana

		self.etiq_user.grid(column=0, row=1)
		self.ctext_user.grid(column=1, row=1, columnspan=2)

		self.etiq_clave.grid(column=0, row=2)
		self.ctext_clave.grid(column=1, row=2, columnspan=2)

		self.etiq_ip.grid(column=0, row=3)
		self.ctext_ip.grid(column=1, row=3, columnspan=2)

		self.connect_ssh.grid(column=0, row=4, columnspan=3)

		self.quit.grid(column=0, row=5, columnspan=3)

	def say_hi(self):
		print("\nHola!\n\nIntegrantes:\nDarwin\nEdwin\nAlonso\nKarol")

	def connect(self):#Establece conexion via ssh
		self.client=paramiko.SSHClient()
		self.client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
		self.client.connect('192.168.0.106', username='darwin', password='holahola')
		self.sftp = self.client.open_sftp()
		#self.client.connect(self.ctext_ip.get(), username=self.ctext_user.get(), password=self.ctext_clave.get())
		print("\nConectado!")
		self.create_widgets_connect()
		

	def create_widgets_connect(self):
		self.connect_interface = tk.Toplevel(self)
		self.connect_interface.geometry("400x400")
		self.connect_interface.resizable(0,0)

		self.start_app = tk.Button(self.connect_interface)
		self.start_app["text"] = "Iniciar aplicacion."
		self.start_app["command"] = self.startapp
		self.start_app.grid(column=1, row=0, columnspan=3)

		self.end_app = tk.Button(self.connect_interface)
		self.end_app["text"] = "Terminar ejecucion de aplicacion."
		self.end_app["command"] = self.endapp
		self.end_app.grid(column=1, row=1, columnspan=3)

		self.read_inf = tk.Button(self.connect_interface)
		self.read_inf["text"] = "Leer informe."
		self.read_inf["command"] = self.read
		self.read_inf.grid(column=1, row=2, columnspan=3)

		self.watch_video = tk.Button(self.connect_interface)
		self.watch_video["text"] = "Ver video."
		self.watch_video["command"] = self.watchvideo
		self.watch_video.grid(column=1, row=3, columnspan=3)

		self.quit2 = tk.Button(self.connect_interface, text="SALIR", fg="red")
		self.quit2["command"] = self.disconnect
		self.quit2.grid(column=1, row=4, columnspan=3)

		self.master.wait_window(self.connect_interface)

	def startapp(self):#para iniciar sniffer
		print("\nIniciando aplicacion!")
		self.client.exec_command('python3 /home/darwin/proyecto3/sniffer_trial.py')

	def endapp(self):#para iniciar sniffer
		print("\nTerminando ejecucion!")
		self.client.exec_command('^C')

	def read(self):#Para leer informe generado por el sniffer (sin hacer)
		print("\nAbriendo informe!")
		#Direccion = subprocess.call(['pwd'])
		#self.sftp.get('/home/darwin/Descargas/Informe.txt', '/home/darwin/proyecto3/informe.txt')
		self.sftp.get('/home/darwin/proyecto3/Informe.txt', '/home/darwin/proyecto3/informeprueba.txt')
		subprocess.call(['nano','-v','informeprueba.txt'])

	def watchvideo(self):#Para ver un video generado por el sniffer (sin hacer)
		print("\nReproduciendo video!")
		self.sftp.get('/home/darwin/proyecto3/footage.avi', '/home/darwin/proyecto3/videoprueba.avi')
		subprocess.call(['mplayer','videoprueba.avi'])

	def disconnect(self):#Salir de la app
		print("\nCerrando conexion!")
		self.connect_interface.destroy()
		self.client.close()

	def exit(self):#Salir de la app
		print("\nSaliendo!\n")
		self.master.destroy()

root = tk.Tk()
app = Application(master=root)
app.mainloop()