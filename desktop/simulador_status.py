# Arquivo: simulador_status.py

import requests
import random
from datetime import datetime, timedelta

STATUS_API_URL = "http://18.223.171.40:8181/cxf/m2fot-status/fot-gateway-status/"

def gerar_status(gateway_mac, timestamp, estado_gateway):
    """Gera um objeto de status no formato exigido pela API com base em estado prévio"""
    status_ativo = random.random() > 0.1  # 90% chance de estar ativo

    baterry = max(0.0, round(estado_gateway["baterryLevel"] - random.uniform(0.001, 0.005), 2))
    memory = min(1.0, max(0.0, round(estado_gateway["usedMemory"] + random.uniform(-0.05, 0.05), 2)))
    cpu = min(1.0, max(0.0, round(estado_gateway["usedProcessor"] + random.uniform(-0.05, 0.05), 2)))

    return {
        "date": {
            "year": timestamp.year,
            "month": timestamp.month,
            "dayOfMonth": timestamp.day,
            "hourOfDay": timestamp.hour,
            "minute": timestamp.minute,
            "second": timestamp.second
        },
        "gateway": {
            "mac": gateway_mac,
            "status": status_ativo
        },
        "baterryLevel": baterry,
        "usedMemory": memory,
        "usedProcessor": cpu
    }

def enviar_status_para_api(status_data):
    """Envia um registro de status à API de armazenamento"""
    try:
        resposta = requests.post(STATUS_API_URL, json=status_data)
        resposta.raise_for_status()
        print(f"✅ Status enviado: {status_data['gateway']['mac']} @ {status_data['date']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Falha ao enviar status: {e}")

def gerar_status_simulado(macs, total_status=5):
    """Gera os dados simulados de status para todos os gateways"""
    tempo = datetime.now()
    todos_os_status = []

    estados = {
        mac: {
            "baterryLevel": round(random.uniform(0.7, 1.0), 2),
            "usedMemory": round(random.uniform(0.2, 0.5), 2),
            "usedProcessor": round(random.uniform(0.2, 0.5), 2)
        }
        for mac in macs
    }

    for mac in macs:
        estado_atual = estados[mac]
        for _ in range(total_status):
            tempo += timedelta(seconds=1)
            status = gerar_status(mac, tempo, estado_atual)
            estado_atual.update({
                "baterryLevel": status["baterryLevel"],
                "usedMemory": status["usedMemory"],
                "usedProcessor": status["usedProcessor"]
            })
            todos_os_status.append(status)

    return todos_os_status

def perguntar_e_enviar(status_list):
    """Pergunta ao usuário se deseja enviar os dados simulados"""
    resposta = input("\n❓ Deseja enviar os dados simulados para a API? (s/n): ").strip().lower()
    if resposta == 's':
        print("\n📤 Enviando dados de status para a API...")
        for status in status_list:
            enviar_status_para_api(status)
        print("\n✔️ Envio concluído.")
    else:
        print("⏹️ Envio cancelado pelo usuário.")
