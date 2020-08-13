
import time
import tkinter as tk
#import subprocess #para ejecutar en terminal de computador
import paramiko #para ejecutar remoto
from getpass import getpass

class Application(tk.Frame):
	def __init__(self, master=None):#crea la raiz o ventana principal de la app
		super().__init__(master)
		self.master = master
		self.master.geometry("800x600")
		self.master.resizable(0,0)
		self.master.title("applicacion de seguridad")
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

		self.start_app = tk.Button(self)
		self.start_app["text"] = "Iniciar aplicacion."
		self.start_app["command"] = self.startapp

		self.read_inf = tk.Button(self)
		self.read_inf["text"] = "Leer informe."
		self.read_inf["command"] = self.read

		self.etiq_video = tk.Label(self, text="Video a ver:", font="Arial")
		self.video = str   
		self.ctext_video = tk.Entry(self, textvariable=self.video,width=30)

		self.watch_video = tk.Button(self)
		self.watch_video["text"] = "Ver video."
		self.watch_video["command"] = self.watchvideo

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

		self.start_app.grid(column=0, row=5, columnspan=3)

		self.read_inf.grid(column=0, row=6, columnspan=3)

		self.etiq_video.grid(column=0, row=7)
		self.ctext_video.grid(column=1, row=7, columnspan=2)

		self.watch_video.grid(column=0, row=8, columnspan=3)

		self.quit.grid(column=0, row=9, columnspan=3)

	def say_hi(self):
		print("\nHola!\n\nIntegrantes:\nDarwin\nEdwin\nAlonso\nKarol")

	def connect(self):#Establece conexion via ssh
		print("\nSe establece la conexion!")
		client=paramiko.SSHClient()
		client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
		client.connect(self.ctext_ip.get(), username=self.ctext_user.get(), password=self.ctext_clave.get())
		print("\nConectado!")
		stdin, stdout, stderr = client.exec_command('ls')
		result = stdout.read().decode()
		print(result)
		print("\nLa conexion es correcta.")
		print("\nCerrando conexion.")
		client.close()

	def startapp(self):#para iniciar sniffer (sin hacer)
		print("\nIniciando aplicacion!")
		client=paramiko.SSHClient()
		client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
		client.connect(self.ctext_ip.get(), username=self.ctext_user.get(), password=self.ctext_clave.get())
		print("\nConectado!")
		stdin, stdout, stderr = client.exec_command('python3 /usr/bin/python-sniffer.py')
		result = stdout.read().decode()
		print(result)
		print("\nCerrando conexion.")
		client.close()

	def read(self):#Para leer informe generado por el sniffer (sin hacer)
		print("\nAbriendo informe!")
		client=paramiko.SSHClient()
		client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
		client.connect(self.ctext_ip.get(), username=self.ctext_user.get(), password=self.ctext_clave.get())
		print("\nConectado!")
		stdin, stdout, stderr = client.exec_command('nano -v /usr/bin/Informe.txt') #abre solo lectura
		result = stdout.read().decode()
		print(result)
		print("\nCerrando conexion.")
		client.close()

	def watchvideo(self):#Para ver un video generado por el sniffer (sin hacer)
		print("\nReproduciendo video!")
		client=paramiko.SSHClient()
		client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
		client.connect(self.ctext_ip.get(), username=self.ctext_user.get(), password=self.ctext_clave.get())
		print("\nConectado!")
		stdin, stdout, stderr = client.exec_command(['omxplayer', "/usr/bin/"+self.ctext_video.get()])
		result = stdout.read().decode()
		print(result)
		print("\nCerrando conexion.")
		client.close()

	def exit(self):#Salir de la app
		print("\nSaliendo!\n")
		self.master.destroy()

root = tk.Tk()
app = Application(master=root)
app.mainloop()