#!/usr/bin/env python3

import subprocess
import threading
import time
import signal
import sys
import os

class QuizRunner:
    def __init__(self):
        self.server_process = None
        self.client_processes = []
        self.server_output = []
        self.game_finished = False
        self.num_clients = 5
        
    def run_server(self):
        print("🖥️  Iniciando servidor...")
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, "servidor_udp.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            print(f"[SERVIDOR] Processo iniciado com PID: {self.server_process.pid}")
            
            while True:
                output = self.server_process.stdout.readline()
                if output == '' and self.server_process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    self.server_output.append(line)
                    print(f"[SERVIDOR] {line}")
                    
                    if "RESULTADO FINAL" in line or "Obrigado por participar" in line:
                        self.game_finished = True
                        
        except Exception as e:
            print(f"❌ Erro no servidor: {e}")

    def run_client_instance(self, client_id):
        try:
            process = subprocess.Popen(
                [sys.executable, "clientes_udp.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True
            )
            
            self.client_processes.append(process)
            print(f"✅ Cliente {client_id} iniciado (PID: {process.pid})")
            
            process.wait()
                    
        except Exception as e:
            print(f"❌ Erro no cliente {client_id}: {e}")

    def run_multiple_clients(self):
        print("⏳ Aguardando servidor inicializar...")
        time.sleep(5)
        
        print(f" Iniciando {self.num_clients} clientes em paralelo...")
        
        client_threads = []
        for i in range(self.num_clients):
            thread = threading.Thread(
                target=self.run_client_instance, 
                args=(i+1,), 
                daemon=True
            )
            client_threads.append(thread)
            thread.start()
            time.sleep(1)
        
        print("✅ Todos os clientes iniciados!")
        
        for thread in client_threads:
            thread.join()

    def extract_final_results(self):
        print("\n" + "="*60)
        print(" RESULTADO FINAL DO JOGO")
        print("="*60)
        
        if not self.server_output:
            print("❌ Nenhum output do servidor capturado!")
            return
        
        final_scores = []
        in_scoreboard = False
        
        for line in self.server_output:
            if "RESULTADO FINAL" in line or "Pontuações atuais dos clientes" in line:
                in_scoreboard = True
                print(f"\n{line}")
            elif in_scoreboard and "pontos" in line:
                print(line)
                final_scores.append(line)
            elif in_scoreboard and "===" in line:
                print(line)
            elif in_scoreboard and not line.strip():
                continue
            elif in_scoreboard:
                in_scoreboard = False
        
        if not final_scores:
            print("📊 Último placar disponível:")
            for line in reversed(self.server_output):
                if "pontos" in line and "Cliente" in line:
                    print(line)
                elif "===" in line and "Pontuações" in line:
                    break
        
        print("\n" + "="*60)
        print("🎯 JOGO FINALIZADO!")
        print("="*60)

    def signal_handler(self, sig, frame):
        print("\n Encerrando sistema...")
        if self.server_process:
            self.server_process.terminate()
        for process in self.client_processes:
            if process:
                process.terminate()
        sys.exit(0)

    def main(self):
        print("🎯 SISTEMA DE QUIZ - EXECUÇÃO SIMULTÂNEA")
        print("=" * 60)
        print("📋 Este script executa automaticamente:")
        print(f"   • Servidor (servidor_udp.py) - Output visível")
        print(f"   • {self.num_clients} Clientes em paralelo (clientes_udp.py) - Silenciosos")
        print("   • Exibe resultado final")
        print("=" * 60)
        
        if not os.path.exists("servidor_udp.py"):
            print("❌ Arquivo servidor.py não encontrado!")
            return
        if not os.path.exists("clientes_udp.py"):
            print("❌ Arquivo clientes.py não encontrado!")
            return
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        server_thread = threading.Thread(target=self.run_server, daemon=True)
        clients_thread = threading.Thread(target=self.run_multiple_clients, daemon=True)
        
        server_thread.start()
        clients_thread.start()
        
        print("✅ Sistema iniciado! Aguardando finalização...")
        print("=" * 60)
        
        try:
            server_thread.join()
            clients_thread.join()
            
            time.sleep(3)
            
            self.extract_final_results()
            
        except KeyboardInterrupt:
            print("\n🛑 Sistema encerrado pelo usuário.")

def main():
    runner = QuizRunner()
    runner.main()

if __name__ == "__main__":
    main()