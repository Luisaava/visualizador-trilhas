from servicos_tecnicos.persistencia import PersistenciaJSON
from dominio.usuarios import Moderador
from dominio.trilhas import trilhas # Dicionário global de trilhas oficiais


class InterfaceModerador:
    def __init__(self, persistencia: PersistenciaJSON):
        self.persistencia = persistencia
        self.moderador_ativo = Moderador()

    def exibir_painel(self):
        while True:
            print("\n=== PAINEL DO MODERADOR ===")
            print("1. Ver lista de todos os usuários do sistema")
            print("2. Ver e aprovar trilhas pendentes")
            print("0. Deslogar (Voltar ao menu inicial)")

            opcao = input("Escolha: ").strip()

            if opcao == "1":
                todos = self.persistencia.carregar_todos()
                print(f"\nUsuários cadastrados ({len(todos)}):")
                for u in todos.keys():
                    print(f" - {u}")
            elif opcao == "2":
                self.gerenciar_trilhas_pendentes()
            elif opcao == "0":
                print("Saindo do painel de moderação...")
                break
            else:
                print("Opção inválida.")

    def gerenciar_trilhas_pendentes(self):
        pendentes = list(Moderador.trilhasAprovacao.values())

        if not pendentes:
            print("\nNão há nenhuma trilha aguardando aprovação no momento.")
            return

        print("\n=== TRILHAS PENDENTES DE APROVAÇÃO ===")
        for i, trilha in enumerate(pendentes, start=1):
            print(f"{i} - Nome: {trilha.nome} | Criador: {trilha.criador.nome} | Dificuldade: {trilha.dificuldade}")

        escolha = input("\nEscolha o número da trilha para aprovar (ou 0 para cancelar): ").strip()

        if escolha == '0':
            return

        if escolha.isdigit() and 1 <= int(escolha) <= len(pendentes):
            trilha_escolhida = pendentes[int(escolha) - 1]
            
            print(f"\nDeseja mesmo aprovar a trilha '{trilha_escolhida.nome}'?")
            print("1 - Sim   2 - Não (Apenas voltar)")
            acao = input("Escolha: ").strip()

            if acao == "1":
                #chama aprovacao do moderador
                sucesso, msg = self.moderador_ativo.aprovarTrilha(trilha_escolhida.nome, trilhas)
                print(f"\n{msg}")
            else:
                print("\nAção cancelada.")
        else:
            print("\nOpção inválida.")