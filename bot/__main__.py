from bot import TelegramBot
from bot.server import server
from bot.modules.database.json_db import init_json
from bot.modules.backup import restore_db, start_backup_loop
from bot.config import Server
import asyncio
import os
import socket
import subprocess
from hydrogram import idle

def kill_process_on_port(port):
    """Encerra qualquer processo que esteja usando a porta especificada."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                print(f"Porta {port} em uso. Tentando liberar...")
                if os.name == 'nt': # Windows
                    cmd = f"powershell -Command \"Stop-Process -Id (Get-NetTCPConnection -LocalPort {port}).OwningProcess -Force\""
                    subprocess.run(cmd, shell=True, capture_output=True)
                else: # Linux/Unix
                    subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True)
                print(f"Porta {port} liberada.")
    except Exception as e:
        print(f"Erro ao tentar liberar porta {port}: {e}")

async def start_services():
    # Inicializa o JSON DB
    init_json()
    
    # Inicia o bot do Telegram
    await TelegramBot.start()
    
    # Restaura o banco de dados do canal se necessário
    await restore_db()
    
    # Inicia o servidor web e o loop de backup como tarefas no mesmo loop do bot
    asyncio.create_task(server.serve())
    asyncio.create_task(start_backup_loop())
    
    print("Bot started!")
    
    # Mantém o bot rodando e aguarda sinais de interrupção (SIGINT, SIGTERM)
    await idle()
    
    # Encerramento gracioso após o idle() ser interrompido
    print("Encerrando servidor e bot...")
    if server.started:
        await server.shutdown()
    
    await TelegramBot.stop()
    print("Bot desligado com sucesso.")

if __name__ == '__main__':
    # Limpa a porta antes de qualquer coisa
    kill_process_on_port(Server.PORT)
    
    # Usa o loop padrão do asyncio de forma segura
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        # Garante que o loop seja fechado se não estiver rodando
        if not loop.is_running():
            loop.close()
