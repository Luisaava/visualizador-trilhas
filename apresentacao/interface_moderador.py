from servicos_tecnicos.persistencia import PersistenciaJSON


class InterfaceModerador:
    def __init__(self, persistencia: PersistenciaJSON):
        self.persistencia = persistencia

    def exibir_painel(self):
        while True:
            print("\n=== PAINEL DO MODERADOR ===")
            print("1. Ver lista de todos os usuários do sistema")
            print("2. Deslogar (Voltar ao menu inicial)")
            opcao = input("Escolha: ").strip()

            if opcao == "1":
                todos = self.persistencia.carregar_todos()
                print(f"\nUsuários cadastrados ({len(todos)}):")
                for u in todos.keys():
                    print(f" - {u}")
            elif opcao == "2":
                print("Saindo do painel de moderação...")
                break
            else:
                print("Opção inválida.")