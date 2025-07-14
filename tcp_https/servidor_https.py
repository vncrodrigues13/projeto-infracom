import socket
import threading
import random
import ssl
import os

BUFFER_SIZE = 1024
NUM_CLIENTS = 16

clients = {}
clients_lock = threading.Lock()
client_answers = {}
client_scores = {}
answers_lock = threading.Lock()

quests = [
    {'quest': 'Qual é a capital do Brasil?', 'answer': 'B', 'options': [{'A': 'São Paulo'}, {'B': 'Brasília'}, {'C': 'Rio de Janeiro'}, {'D': 'Salvador'}]},
    {'quest': 'Qual é o elemento químico representado por H?', 'answer': 'A', 'options': [{'A': 'Hidrogênio'}, {'B': 'Hélio'}, {'C': 'Hidroxila'}, {'D': 'Hematita'}]},
    {'quest': 'Quem escreveu "Dom Casmurro"?', 'answer': 'C', 'options': [{'A': 'José de Alencar'}, {'B': 'Carlos Drummond'}, {'C': 'Machado de Assis'}, {'D': 'Clarice Lispector'}]},
    {'quest': 'Qual planeta é o terceiro a partir do Sol?', 'answer': 'D', 'options': [{'A': 'Vênus'}, {'B': 'Marte'}, {'C': 'Mercúrio'}, {'D': 'Terra'}]},
    {'quest': 'Em que continente fica o Egito?', 'answer': 'A', 'options': [{'A': 'África'}, {'B': 'Ásia'}, {'C': 'Europa'}, {'D': 'América'}]},
    {'quest': 'Qual é o maior oceano do mundo?', 'answer': 'B', 'options': [{'A': 'Atlântico'}, {'B': 'Pacífico'}, {'C': 'Índico'}, {'D': 'Ártico'}]},
    {'quest': 'Quanto é 9 x 7?', 'answer': 'C', 'options': [{'A': '56'}, {'B': '72'}, {'C': '63'}, {'D': '67'}]},
    {'quest': 'Qual destes é um mamífero?', 'answer': 'A', 'options': [{'A': 'Golfinho'}, {'B': 'Pinguim'}, {'C': 'Tubarão'}, {'D': 'Camarão'}]},
    {'quest': 'Quem foi o primeiro homem a pisar na Lua?', 'answer': 'D', 'options': [{'A': 'Buzz Aldrin'}, {'B': 'Yuri Gagarin'}, {'C': 'Michael Collins'}, {'D': 'Neil Armstrong'}]},
    {'quest': 'Qual língua é falada no Japão?', 'answer': 'B', 'options': [{'A': 'Chinês'}, {'B': 'Japonês'}, {'C': 'Coreano'}, {'D': 'Tailandês'}]}
]

next_client_id = 1
next_client_id_lock = threading.Lock()

final_scores = {}
final_scores_lock = threading.Lock()

def create_self_signed_cert():
    cert_file = "server.crt"
    key_file = "server.key"
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("Gerando certificado SSL auto-assinado...")
        os.system(f'openssl req -x509 -newkey rsa:4096 -keyout {key_file} -out {cert_file} -days 365 -nodes -subj "/C=BR/ST=SP/L=SP/O=Quiz/CN=localhost"')
        print("Certificado SSL gerado com sucesso!")
    
    return cert_file, key_file

def get_next_question(previous_index):
    new_index = random.randint(0, len(quests) - 1)
    while new_index == previous_index:
        new_index = random.randint(0, len(quests) - 1)
    return new_index, quests[new_index]

def format_question(question_dict):
    lines = [question_dict['quest']]
    for opt in question_dict['options']:
        for key, value in opt.items():
            lines.append(f"{key}) {value}")
    return '\n'.join(lines)

def print_scoreboard():
    with final_scores_lock:
        if not final_scores:
            print("[Nenhum cliente respondeu ainda]")
            return
        print("\n=== Pontuações atuais dos clientes ===")
        sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        for name, score in sorted_scores:
            print(f"{name}: {score:.2f} pontos")
        print("=====================================\n")

def handle_client(client_socket, address):
    global next_client_id

    with next_client_id_lock:
        client_name = f"Cliente {next_client_id}"
        next_client_id += 1

    with clients_lock:
        clients[client_name] = client_socket
    with answers_lock:
        client_answers[client_name] = []
        client_scores[client_name] = 0.0
    with final_scores_lock:
        final_scores[client_name] = 0.0

    print(f"[+] {client_name} conectado via HTTPS ({address[0]}:{address[1]})")

    previous_index = -1
    score_decrement = 0.0
    max_score = 1.0

    try:
        for _ in range(5):
            previous_index, question = get_next_question(previous_index)
            formatted = format_question(question)
            client_socket.sendall(formatted.encode())

            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            received = data.decode().strip().upper()
            print(f"[{client_name}] Respondeu: {received}")

            with answers_lock:
                client_answers[client_name].append({'question': question['quest'], 'answer': received})

                if received == question['answer']:
                    score = max_score - score_decrement
                    if score < 0:
                        score = 0
                    client_scores[client_name] += score
                    with final_scores_lock:
                        final_scores[client_name] = client_scores[client_name]
                    score_decrement += 0.1

        client_socket.sendall(b"Obrigado por responder. Encerrando.")
    except Exception as e:
        print(f"[{client_name}] Erro: {e}")
    finally:
        with clients_lock:
            if client_name in clients:
                del clients[client_name]
        with answers_lock:
            print(f"[{client_name}] Respostas coletadas e pontuação final: {client_scores[client_name]:.2f} pontos")
            if client_name in client_answers:
                del client_answers[client_name]
            if client_name in client_scores:
                del client_scores[client_name]
        client_socket.close()
        print(f"[-] {client_name} desconectado.")

        print_scoreboard()

def start_server(host='127.0.0.1', port=12345):
    cert_file, key_file = create_self_signed_cert()
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(NUM_CLIENTS)
    
    ssl_server = context.wrap_socket(server, server_side=True)
    
    print(f"[*] Servidor HTTPS listening on {host}:{port}")
    print(f"[*] Certificado SSL: {cert_file}")
    print(f"[*] Chave privada: {key_file}")

    try:
        while True:
            client_socket, address = ssl_server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Servidor HTTPS encerrado.")
    finally:
        ssl_server.close()
        server.close()

if __name__ == "__main__":
    start_server()
