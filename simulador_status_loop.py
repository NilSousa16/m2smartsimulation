# Arquivo: simulador_status_loop.py

import requests
import random
import time
from datetime import datetime
from simulador_status import gerar_status, enviar_status_para_api
from simulador_gateway import obter_macs

def iniciar_simulacao_em_loop(intervalo_segundos=5):
    """Inicia a simulação contínua de envio de status para cada gateway"""
    print(f"\n⏳ Iniciando simulação contínua com intervalo de {intervalo_segundos} segundos...")
    
    macs = obter_macs()
    if not macs:
        print("⚠️ Nenhum MAC de gateway encontrado. Encerrando simulação.")
        return

    estados = {
        mac: {
            "baterryLevel": round(random.uniform(0.7, 1.0), 2),
            "usedMemory": round(random.uniform(0.2, 0.5), 2),
            "usedProcessor": round(random.uniform(0.2, 0.5), 2)
        }
        for mac in macs
    }

    try:
        while True:
            tempo = datetime.now()
            for mac in macs:
                estado = estados[mac]
                status = gerar_status(mac, tempo, estado)
                enviar_status_para_api(status)

                # Atualiza o estado para a próxima iteração
                estado.update({
                    "baterryLevel": status["baterryLevel"],
                    "usedMemory": status["usedMemory"],
                    "usedProcessor": status["usedProcessor"]
                })

            time.sleep(intervalo_segundos)
    except KeyboardInterrupt:
        print("\n🛑 Simulação contínua encerrada pelo usuário com Ctrl + C.")
