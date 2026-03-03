from bot import TelegramBot
from bot.server import server
from bot.modules.database.json_db import init_json
from bot.modules.backup import restore_db, start_backup_loop
from bot.config import Server
import asyncio
import os
import signal
import socket
import subprocess

def kill_process_on_port(port):
    """Encerra qualquer processo que esteja usando a porta especificada."""
    try:
        # Tenta encontrar o PID do processo usando a porta
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                print(f"Porta {port} em uso. Tentando liberar...")
                if os.name == 'nt': # Windows
                    # Comando PowerShell para matar o processo na porta
                    cmd = f"powershell -Command \"Stop-Process -Id (Get-NetTCPConnection -LocalPort {port}).OwningProcess -Force\""
                    subprocess.run(cmd, shell=True, capture_output=True)
                else: # Linux/Unix
                    # Comando fuser para matar o processo na porta
                    subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True)
                print(f"Porta {port} liberada.")
    except Exception as e:
        print(f"Erro ao tentar liberar porta {port}: {e}")

async def main():
    # Limpa a porta antes de iniciar o servidor
    kill_process_on_port(Server.PORT)
    
    init_json()
    await TelegramBot.start()
    await restore_db()
    
    # Inicia o servidor web e o loop de backup como tarefas em segundo plano
    loop = asyncio.get_running_loop()
    server_task = loop.create_task(server.serve())
    backup_task = loop.create_task(start_backup_loop())
    
    print("Bot started!")
    
    # Evento para manter o bot rodando
    stop_event = asyncio.Event()
    
    def signal_handler():
        print("\nSinal de interrupção recebido. Desligando...")
        stop_event.set()

    # Registra handlers para SIGINT e SIGTERM no Linux
    if os.name != 'nt':
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, signal_handler)

    try:
        # Espera o evento de parada ou interrupção por teclado
        await stop_event.wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        signal_handler()
    
    # Encerramento gracioso
    print("Encerrando servidor e bot...")
    if server.started:
        await server.shutdown()
    
    # Cancela as tarefas em segundo plano
    backup_task.cancel()
    
    await TelegramBot.stop()
    print("Bot desligado com sucesso.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erro fatal: {e}")
