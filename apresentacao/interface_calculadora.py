from aplicacao.sessao_calculo import SessaoCalculo

class InterfaceCalculadora:
    def __init__(self, app_service: SessaoCalculo):
        self.app = app_service

    def exibir_menu(self):
        while True:
            print("\n=== CALCULADORA CLI ===")
            print("1. Realizar Cálculo")
            print("2. Ver Histórico")
            print("3. Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self._menu_calcular()
            elif opcao == "2":
                self._menu_historico()
            elif opcao == "3":
                print("Encerrando...")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def _menu_calcular(self):
        op1 = float(input("Digite o 1º número: "))
        operador = input("Digite o operador (+, -, *, /): ").strip()
        op2 = float(input("Digite o 2º número: "))

        calculo = self.app.realizar_calculo(op1, operador, op2)
        print(f"\n-> Resultado: {calculo.operando1} {calculo.operador} {calculo.operando2} = {calculo.resultado}")

    def _menu_historico(self):
        historico = self.app.obter_historico()
        print("\n--- HISTÓRICO DE CÁLCULOS ---")
        if not historico:
            print("Nenhum cálculo registrado ainda.")
            return

        for item in historico:
            print(f"[{item.data_hora}] {item.operando1} {item.operador} {item.operando2} = {item.resultado}")