from simulador_gateway import gerar_gateways_simulados, obter_macs
from simulador_status import gerar_status_simulado, perguntar_e_enviar
from simulador_status_loop import iniciar_simulacao_em_loop
from simulador_dispositivo import gerar_dispositivos_simulados
from simulador_status_dispositivo import gerar_status_simulado_dispositivos
from simulador_status_dispositivo_loop import iniciar_simulacao_status_dispositivo_em_loop
from simulador_loop_geral import iniciar_simulacoes_em_loop


def menu():
    while True:
        print("\n====== MENU SIMULADOR ======")
        print("1 - Inserir novos - gateways")
        print("2 - Inserir status simulados - gateways")
        print("3 - Executar status contínuo (loop) - gateways")
        print("4 - Inserir novos - dispositivos")
        print("5 - Inserir status simulados - dispositivos")
        print("6 - Executar status contínuo (loop) - dispositivos")
        print("7 - Executar status contínuo (loop) - gateways e dispositivos")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            total = input("🔢 Quantos gateways deseja inserir? ").strip()
            if total.isdigit():
                gerar_gateways_simulados(int(total), central_lat=-13.005, central_lon=-38.516, raio_km=1)
            else:
                print("⚠️ Entrada inválida.")

        elif opcao == '2':
            macs = obter_macs()
            if not macs:
                print("⚠️ Nenhum gateway encontrado.")
            else:
                status = gerar_status_simulado(macs, total_status=5)
                perguntar_e_enviar(status)

        elif opcao == '3':
            intervalo = input("⏱️ Intervalo em segundos entre os envios: ").strip()
            if intervalo.isdigit() and int(intervalo) > 0:
                iniciar_simulacao_em_loop(int(intervalo))
            else:
                print("⚠️ Intervalo inválido.")

        elif opcao == '4':
            total = input("🔢 Quantos dispositivos deseja inserir? ").strip()
            if total.isdigit():
                gerar_dispositivos_simulados(int(total), raio_km=1)
            else:
                print("⚠️ Entrada inválida.")

        elif opcao == '5':
            total = input("🔢 Quantas entradas de status por dispositivo? ").strip()
            if total.isdigit():
                gerar_status_simulado_dispositivos(total_status=int(total))
            else:
                print("⚠️ Entrada inválida.")

        elif opcao == '6':
            intervalo = input("⏱️ Intervalo em segundos entre os envios: ").strip()
            if intervalo.isdigit() and int(intervalo) > 0:
                iniciar_simulacao_status_dispositivo_em_loop(int(intervalo))
            else:
                print("⚠️ Intervalo inválido.")
        
        elif opcao == '7':
            intervalo_gw = input("⏱️ Intervalo em segundos para os gateways: ").strip()
            intervalo_dev = input("⏱️ Intervalo em segundos para os dispositivos: ").strip()

            if intervalo_gw.isdigit() and intervalo_dev.isdigit() and int(intervalo_gw) > 0 and int(intervalo_dev) > 0:
                iniciar_simulacoes_em_loop(int(intervalo_gw), int(intervalo_dev))
            else:
                print("⚠️ Intervalo inválido.")

        elif opcao == '0':
            print("👋 Encerrando simulador.")
            break

        else:
            print("⚠️ Opção inválida.")


if __name__ == "__main__":
    menu()
