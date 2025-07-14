from socket import *
import threading
from quest import get_next_question


BUFFER_SIZE=1024
clients = {}
clients_lock = threading.Lock()




def handle_client(client_socket, address):
   host, port = address
   print(f"[+] New connection from {host}:{port}")


   # Save client info
   with clients_lock:
       clients[(host, port)] = client_socket




def start_server(host='0.0.0.0', port=12345):
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind((host, port))
   server.listen(5)
   print(f"[*] Server listening on {host}:{port}")


   while True:
       client_socket, address = server.accept()
       client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
       client_thread.daemon = True
       client_thread.start()



