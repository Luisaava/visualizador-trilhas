from __future__ import annotations
from dominio.usuarios import Moderador
from aplicacao.sessao_moderacao import SessaoAprovarTrilha


class InterfaceModerador:
    def __init__(self, moderador_ativo: Moderador):
        self.__moderador_ativo: Moderador = moderador_ativo
        self.__sessao_aprovacao: SessaoAprovarTrilha = SessaoAprovarTrilha()

    def exibirPainel(self) -> None:
        while True:
            print(f"\n=== PAINEL DO MODERADOR ({self.__moderador_ativo.nome}) ===")
            print("1 - Ver lista de todos os usuários do sistema")
            print("2 - Ver e aprovar/rejeitar trilhas pendentes")
            print("0 - Deslogar (Voltar ao menu inicial)")

            opcao = input("Escolha: ").strip()

            if opcao == "1":
                try:
                    todos = self.__sessao_aprovacao.listarUsuarios()
                    print(f"\nUsuários cadastrados ({len(todos)}):")
                    for u in todos:
                        papel = "Moderador" if isinstance(u, Moderador) else "Usuário"
                        print(f" - [{u.id}] {u.nome} ({papel})")
                except Exception as e:
                    print(f"\nErro ao listar usuários: {e}")
            elif opcao == "2":
                self.gerenciarTrilhasPendentes()
            elif opcao == "0":
                print("Saindo do painel de moderação...")
                break
            else:
                print("Opção inválida.")

    def gerenciarTrilhasPendentes(self) -> None:
        try:
            pendentes = self.__sessao_aprovacao.listarTrilhasPendentes()
        except Exception as e:
            print(f"\nErro ao buscar trilhas pendentes: {e}")
            return

        if not pendentes:
            print("\nNão há nenhuma trilha aguardando aprovação no momento.")
            return

        print("\n=== TRILHAS PENDENTES DE APROVAÇÃO ===")
        for i, trilha in enumerate(pendentes, start=1):
            print(
                f"{i} - Nome: {trilha.nome} | Criador: {trilha.criador.nome} | "
                f"Dificuldade: {trilha.dificuldade}/10 | Distância: {trilha.comprimento:.1f} km"
            )

        escolha = input("\nEscolha o número da trilha (ou 0 para cancelar): ").strip()
        if escolha == "0":
            return

        if not (escolha.isdigit() and 1 <= int(escolha) <= len(pendentes)):
            print("\nOpção inválida.")
            return

        trilha_escolhida = pendentes[int(escolha) - 1]
        print(f"\nTrilha selecionada: '{trilha_escolhida.nome}'")
        print("1 - Aprovar   2 - Rejeitar   0 - Cancelar")
        acao = input("Escolha: ").strip()

        try:
            if acao == "1":
                self.__sessao_aprovacao.aprovarTrilha(
                    self.__moderador_ativo, trilha_escolhida.nome
                )
                print(f"\nTrilha '{trilha_escolhida.nome}' aprovada com sucesso!")
            elif acao == "2":
                self.__sessao_aprovacao.rejeitarTrilha(trilha_escolhida)
                print(f"\nTrilha '{trilha_escolhida.nome}' rejeitada e removida com sucesso!")
            else:
                print("\nAção cancelada.")
        except Exception as e:
            print(f"\nErro ao processar moderação da trilha: {e}")