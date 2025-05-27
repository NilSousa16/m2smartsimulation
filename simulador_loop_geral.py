import threading
from simulador_status_loop import iniciar_simulacao_em_loop
from simulador_status_dispositivo_loop import iniciar_simulacao_status_dispositivo_em_loop


def iniciar_simulacoes_em_loop(intervalo_gateways, intervalo_dispositivos):
    try:
        # Cria as threads para execução paralela
        thread_gateways = threading.Thread(target=iniciar_simulacao_em_loop, args=(intervalo_gateways,))
        thread_dispositivos = threading.Thread(target=iniciar_simulacao_status_dispositivo_em_loop, args=(intervalo_dispositivos,))

        # Inicia as threads
        thread_gateways.start()
        thread_dispositivos.start()

        print("\n🚀 Simulação contínua de gateways e dispositivos iniciada.")
        print("✅ Pressione CTRL + C para encerrar.\n")

        # Mantém o programa principal aguardando as threads
        thread_gateways.join()
        thread_dispositivos.join()

    except KeyboardInterrupt:
        print("\n⏹️ Simulação encerrada pelo usuário.")
