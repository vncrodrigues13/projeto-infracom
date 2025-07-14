import socket
import threading
import time
import random

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024


def simulate_client(client_id):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (SERVER_HOST, SERVER_PORT)
        
        print(f"[CLIENT {client_id}] Iniciando cliente UDP.")
        
        client_socket.sendto(b"ready", server_address)
        print(f"[CLIENT {client_id}] Registrado no servidor.")

        while True:
            data, server_address = client_socket.recvfrom(BUFFER_SIZE)
            question = data.decode()
            
            if not question:
                print(f"[CLIENT {client_id}] Conexão encerrada pelo servidor.")
                break

            print(f"[CLIENT {client_id}] Pergunta recebida:\n{question}")

            if "Obrigado" in question:
                print(f"[CLIENT {client_id}] Jogo finalizado!")
                break

            answer = random.choice(['A', 'B', 'C', 'D'])
            print(f"[CLIENT {client_id}] Respondendo com: {answer}")
            client_socket.sendto(answer.encode(), server_address)
            time.sleep(1)

    except Exception as e:
        print(f"[CLIENT {client_id}] Erro: {e}")
    finally:
        client_socket.close()
        print(f"[CLIENT {client_id}] Desconectado.")


def main():
    threads = []

    for client_id in range(1, 9):
        t = threading.Thread(target=simulate_client, args=(client_id,))
        t.start()
        threads.append(t)
        time.sleep(0.2)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
