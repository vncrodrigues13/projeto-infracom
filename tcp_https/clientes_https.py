import socket
import threading
import time
import random
import ssl

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024


def simulate_client(client_id):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_client = context.wrap_socket(client_socket, server_hostname=SERVER_HOST)
        
        ssl_client.connect((SERVER_HOST, SERVER_PORT))
        print(f"[CLIENT {client_id}] Conectado ao servidor HTTPS.")

        while True:
            question = ssl_client.recv(BUFFER_SIZE).decode()
            if not question:
                print(f"[CLIENT {client_id}] Conexão encerrada pelo servidor.")
                break

            print(f"[CLIENT {client_id}] Pergunta recebida:\n{question}")

            if "Obrigado" in question:
                break

            answer = random.choice(['A', 'B', 'C', 'D'])
            print(f"[CLIENT {client_id}] Respondendo com: {answer}")
            ssl_client.sendall(answer.encode())
            time.sleep(1)

    except ConnectionRefusedError:
        print(f"[CLIENT {client_id}] Não foi possível conectar ao servidor HTTPS.")
    except ssl.SSLError as e:
        print(f"[CLIENT {client_id}] Erro SSL: {e}")
    except Exception as e:
        print(f"[CLIENT {client_id}] Erro: {e}")
    finally:
        try:
            ssl_client.close()
        except:
            pass
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
