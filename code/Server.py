import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ServerApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Servidor - Chat con los Clientes")

        # Área de chat para mostrar mensajes de los clientes
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state=tk.DISABLED)

        # Campo para escribir la respuesta
        self.msg_entry = tk.Entry(master)
        self.msg_entry.pack(padx=20, pady=5, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_response)

        # Botón para enviar la respuesta
        self.send_button = tk.Button(master, text="Enviar", command=self.send_response)
        self.send_button.pack(padx=20, pady=5)

        # Socket del servidor
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '0.0.0.0'
        self.server_port = 9999
        self.server.bind((self.server_ip, self.server_port))
        self.server.listen(5)

        self.client_socket = None  # Sockets de los clientes
        self.client_address = None
        self.client_message = ""

        self.add_to_chat(f"Servidor escuchando en {self.server_ip}:{self.server_port}")

        # Hilo para aceptar conexiones
        self.accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
        self.accept_thread.start()

    def accept_connections(self):
        """Aceptar conexiones de los clientes."""
        while True:
            self.client_socket, self.client_address = self.server.accept()
            self.add_to_chat(f"Conexión establecida con {self.client_address}")
            threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        """Recibir mensajes del cliente y mostrarlos en la ventana."""
        while True:
            try:
                self.client_message = self.client_socket.recv(1024).decode('utf-8')
                if not self.client_message:
                    break
                self.add_to_chat(f"Cliente {self.client_address}: {self.client_message}")
            except:
                self.add_to_chat(f"Error al recibir mensaje de {self.client_address}")
                break

    def send_response(self, event=None):
        """Enviar respuesta al cliente."""
        response = self.msg_entry.get()
        if response and self.client_socket:
            self.client_socket.send(response.encode('utf-8'))
            self.add_to_chat(f"Tú: {response}")
            self.msg_entry.delete(0, tk.END)

    def add_to_chat(self, message):
        """Agregar mensaje al área de chat."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def close_server(self):
        """Cerrar el servidor y las conexiones."""
        if self.client_socket:
            self.client_socket.close()
        self.server.close()

if _name_ == "_main_":
    root = tk.Tk()
    app = ServerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_server)
    root.mainloop()