from __future__ import annotations
from datetime import datetime, time
from typing import Optional
from dominio.usuarios import Usuario
from dominio.trilhas import Trilha, RegistroIndividual, RegistroGrupo
from aplicacao.sessao_cadastroTrilha import SessaoCadastroTrilha
from aplicacao.sessao_visualizacaoTrilha import SessaoVisualizacaoTrilha
from aplicacao.sessao_buscarTrilhas import SessaoBuscarTrilhas
from aplicacao.sessao_inicioPercurso import (
    SessaoIniciarPercursoIndividual,
    SessaoIniciarPercursoGrupo,
)
from aplicacao.sessao_finalizarPercurso import (
    SessaoFinalizarPercursoIndividual,
    SessaoFinalizarPercursoGrupo,
)
from aplicacao.sessao_amizade import SessaoAmizade
from aplicacao.sessao_excluirConta import SessaoExcluirConta


class InterfaceUsuario:
    def __init__(self, u: Usuario):
        self.__usuarioAtivo: Usuario = u
        self.__sessaoCadastroTrilha: SessaoCadastroTrilha = SessaoCadastroTrilha()
        self.__sessaoVisualizacao: SessaoVisualizacaoTrilha = SessaoVisualizacaoTrilha()
        self.__sessaoBusca: SessaoBuscarTrilhas = SessaoBuscarTrilhas()
        self.__sessaoInicioInd: SessaoIniciarPercursoIndividual = SessaoIniciarPercursoIndividual()
        self.__sessaoInicioGrupo: SessaoIniciarPercursoGrupo = SessaoIniciarPercursoGrupo()
        self.__sessaoFinalizarInd: SessaoFinalizarPercursoIndividual = SessaoFinalizarPercursoIndividual()
        self.__sessaoFinalizarGrupo: SessaoFinalizarPercursoGrupo = SessaoFinalizarPercursoGrupo()
        self.__sessaoAmizade: SessaoAmizade = SessaoAmizade()
        self.__sessaoExcluirConta: SessaoExcluirConta = SessaoExcluirConta()
        self.exibirInterface()

    def exibirInterface(self) -> None:
        print(f"\nBem-vindo(a), {self.__usuarioAtivo.nome}!\n")
        while True:
            self.__usuarioAtivo = self.__sessaoAmizade.recarregarUsuario(self.__usuarioAtivo)
            status_percurso = (
                f" [Percurso ativo: {self.__usuarioAtivo.percursoAtivo.trilha.nome}]"
                if self.__usuarioAtivo.percursoAtivo
                else ""
            )
            print(
                f"""Opções:{status_percurso}
            1 - Exibir perfil e conquistas
            2 - Exibir amigos
            3 - Enviar pedido de amizade
            4 - Exibir e gerenciar pedidos de amizade
            5 - Visualizar todas as trilhas aprovadas
            6 - Buscar trilhas com filtro
            7 - Cadastrar trilha
            8 - Finalizar percurso em andamento
            9 - Excluir minha conta
            0 - Sair
            """
            )
            op: str = input("Digite um número para escolher uma opção: ").strip()
            match op:
                case "1":
                    self.exibirPerfil()
                case "2":
                    self.exibirAmigos()
                case "3":
                    self.enviarPedido()
                case "4":
                    self.gerenciarPedidos()
                case "5":
                    self.visualizarTrilhas()
                case "6":
                    self.buscarTrilhasComFiltro()
                case "7":
                    self.cadastrarTrilha()
                case "8":
                    self.finalizarPercurso()
                case "9":
                    if self.excluirConta():
                        break
                case "0":
                    break
                case _:
                    print("Opção inválida.\n")

    def exibirPerfil(self) -> None:
        print(f"\n=== PERFIL DE {self.__usuarioAtivo.nome} ===")
        print(f"Membro desde: {self.__usuarioAtivo.dataEntrada}")

        if self.__usuarioAtivo.percursoAtivo:
            tipo_p = (
                "Em grupo"
                if isinstance(self.__usuarioAtivo.percursoAtivo, RegistroGrupo)
                else "Individual"
            )
            print(
                f"Percurso em andamento: {self.__usuarioAtivo.percursoAtivo.trilha.nome} ({tipo_p})"
            )

        conquistas = self.__usuarioAtivo.conquistas
        print("\nConquistas desbloqueadas:")
        if not conquistas:
            print("  Nenhuma conquista desbloqueada ainda.")
        else:
            for c in conquistas:
                print(f"  - {c}")

        concluidas = self.__usuarioAtivo.trilhasConcluidas
        if not concluidas:
            print("\nNenhuma trilha concluída ainda.")
        else:
            print("\nRegistros de Trilhas Concluídas:")
            for i, r in enumerate(concluidas, start=1):
                modalidade = (
                    f"Grupo ({r.qtdUsuarios} pessoas)"
                    if isinstance(r, RegistroGrupo)
                    else "Individual"
                )
                print(f"  {i}. Trilha: {r.trilha.nome} [{modalidade}]")
                print(f"     - Tempo levado: {r.tempo}")
                print(f"     - Avaliação dada: {r.avaliacao}")
                print(f"     - Dificuldade percebida: {r.dificuldade}/10")
        print("=" * 45 + "\n")

    def exibirAmigos(self) -> None:
        if not self.__usuarioAtivo.amigos:
            print("\nVocê não possui nenhum amigo.\n")
            return
        print("\n=== MEUS AMIGOS ===")
        for amigo in self.__usuarioAtivo.amigos:
            print(f"- {amigo.nome}")
        print(f"Total: {len(self.__usuarioAtivo.amigos)} amigo(s).\n")

    def enviarPedido(self) -> None:
        nome_alvo = input("Digite o nome do usuário: ").strip()
        try:
            destinatario = self.__sessaoAmizade.buscarUsuarioPorNome(nome_alvo)
            self.__sessaoAmizade.adicionarAmigo(self.__usuarioAtivo, destinatario)
            print(f"\nPedido de amizade enviado para '{destinatario.nome}' com sucesso!\n")
        except Exception as e:
            print(f"\nErro ao enviar pedido de amizade: {e}\n")

    def gerenciarPedidos(self) -> None:
        pedidos = list(self.__usuarioAtivo.pedidosAmizade)
        if not pedidos:
            print("\nNenhum pedido pendente.\n")
            return

        print("\n=== PEDIDOS DE AMIZADE PENDENTES ===")
        for idx, remetente in enumerate(pedidos, start=1):
            print(f"{idx} - {remetente.nome}")

        escolha = input("Digite o número do usuário (ou 0 para voltar): ").strip()
        if escolha == "0":
            return
        if not escolha.isdigit() or not (1 <= int(escolha) <= len(pedidos)):
            print("Opção inválida.\n")
            return

        remetente_obj = pedidos[int(escolha) - 1]
        print(f"\nDeseja aceitar o pedido de {remetente_obj.nome}?")
        print("1 - Sim  2 - Não")
        acao = input("Escolha: ").strip()

        try:
            if acao == "1":
                self.__sessaoAmizade.aceitarPedido(self.__usuarioAtivo, remetente_obj)
                print(f"\nAgora você e '{remetente_obj.nome}' são amigos!\n")
            elif acao == "2":
                self.__sessaoAmizade.recusarPedido(self.__usuarioAtivo, remetente_obj.nome)
                print(f"\nPedido de amizade de '{remetente_obj.nome}' recusado.\n")
            else:
                print("Operação cancelada.\n")
        except Exception as e:
            print(f"\nErro ao gerenciar pedido de amizade: {e}\n")

    def visualizarTrilhas(self) -> None:
        try:
            lista_trilhas = self.__sessaoVisualizacao.listarTrilhasAprovadas()
            self.__selecionarEIniciarTrilha(lista_trilhas, "Trilhas Disponíveis")
        except Exception as e:
            print(f"\nErro ao listar trilhas: {e}\n")

    def buscarTrilhasComFiltro(self) -> None:
        print("\n=== BUSCA DE TRILHAS COM FILTRO ===")
        print("(Pressione ENTER em qualquer campo para ignorar o filtro)")

        try:
            nome = input("Nome da trilha (parcial): ").strip() or None
            local_inicio = input("Local de início: ").strip() or None
            local_fim = input("Local de fim: ").strip() or None

            dificuldade = self.__lerIntOpcional("Dificuldade (1-10): ")
            comp_max = self.__lerFloatOpcional("Comprimento máximo (km): ")
            aval_min = self.__lerFloatOpcional("Avaliação mínima (0.0 a 5.0): ")

            duracao_max: Optional[time] = None
            dur_str = input("Duração máxima (formato 'horas minutos', ex: 2 30): ").strip()
            if dur_str:
                partes = dur_str.split()
                if len(partes) != 2:
                    raise Exception(
                        "Formato de duração inválido. Informe horas e minutos separados por espaço (ex: 2 30)."
                    )
                try:
                    h, m = int(partes[0]), int(partes[1])
                except ValueError:
                    raise Exception("Horas e minutos da duração devem ser números inteiros.")
                if h < 0 or not (0 <= m < 60):
                    raise Exception("Tempo inválido: informe horas >= 0 e minutos entre 0 e 59.")
                duracao_max = time(h, m, 0)

            resultados = self.__sessaoBusca.buscarTrilhas(
                nome=nome,
                localInicio=local_inicio,
                localFim=local_fim,
                dificuldade=dificuldade,
                comprimentoMax=comp_max,
                avaliacaoMin=aval_min,
                duracaoMax=duracao_max,
            )
            self.__selecionarEIniciarTrilha(resultados, "Resultados da Busca")
        except Exception as e:
            print(f"\nErro na busca de trilhas: {e}\n")

    def __selecionarEIniciarTrilha(self, lista_trilhas: list[Trilha], titulo: str) -> None:
        if not lista_trilhas:
            print("\nNenhuma trilha encontrada.\n")
            return

        print(f"\n=== {titulo} ===")
        for i, trilha in enumerate(lista_trilhas, start=1):
            print(
                f"{i} - {trilha.nome} | Dif: {trilha.dificuldade}/10 | "
                f"Dist: {trilha.comprimento:.1f} km | Avaliação: {trilha.avaliacao:.1f}/5.0 | "
                f"Duração média: {trilha.duracaoMedia}"
            )

        escolha = input(
            "\nEscolha o número da trilha para ver detalhes (ou 0 para voltar): "
        ).strip()
        if escolha == "0":
            return

        if not (escolha.isdigit() and 1 <= int(escolha) <= len(lista_trilhas)):
            print("\nOpção inválida.\n")
            return

        trilha_escolhida = lista_trilhas[int(escolha) - 1]
        print("\n" + "=" * 45)
        print(f"DETALHES DA TRILHA: {trilha_escolhida.nome}")
        print("=" * 45)
        print(f"Início: {trilha_escolhida.localInicio}")
        print(f"Fim: {trilha_escolhida.localFim}")
        print(f"Dificuldade (1-10): {trilha_escolhida.dificuldade}")
        print(f"Comprimento: {trilha_escolhida.comprimento:.1f} km")
        print(f"Variação de Altitude: {trilha_escolhida.variacaoAltitude} m")
        print(f"Duração Média: {trilha_escolhida.duracaoMedia}")
        print(f"Avaliação Média: {trilha_escolhida.avaliacao:.1f}/5.0")
        print(f"Criada por: {trilha_escolhida.criador.nome}")
        if trilha_escolhida.aprovadaPor:
            print(f"Aprovada por: {trilha_escolhida.aprovadaPor.nome}")
        print("=" * 45 + "\n")

        print("Deseja iniciar um percurso nesta trilha?")
        print("1 - Iniciar percurso individual")
        print("2 - Iniciar percurso em grupo (com amigos)")
        print("0 - Voltar")
        modo = input("Escolha: ").strip()

        if modo == "1":
            self.iniciarPercursoIndividual(trilha_escolhida)
        elif modo == "2":
            self.iniciarPercursoGrupo(trilha_escolhida)

    def iniciarPercursoIndividual(self, trilha: Trilha) -> None:
        try:
            hora_atual = datetime.now().time().replace(microsecond=0)
            self.__sessaoInicioInd.iniciarPercurso(trilha, hora_atual, self.__usuarioAtivo)
            print(f"\nPercurso individual iniciado na trilha '{trilha.nome}'!\n")
        except Exception as e:
            print(f"\nErro ao iniciar percurso individual: {e}\n")

    def iniciarPercursoGrupo(self, trilha: Trilha) -> None:
        amigos = self.__usuarioAtivo.amigos
        if not amigos:
            print("\nVocê precisa ter amigos cadastrados para iniciar uma trilha em grupo.\n")
            return

        print("\n=== SELECIONE OS AMIGOS PARA O GRUPO ===")
        for idx, amigo in enumerate(amigos, start=1):
            print(f"{idx} - {amigo.nome}")

        entrada = input(
            "Digite os números dos amigos separados por vírgula (ex: 1,2) ou 0 para cancelar: "
        ).strip()
        if entrada == "0" or not entrada:
            return

        try:
            selecionados: list[Usuario] = []
            for parte in entrada.split(","):
                parte = parte.strip()
                if not parte.isdigit() or not (1 <= int(parte) <= len(amigos)):
                    raise Exception(f"Seleção inválida de amigo: '{parte}'.")
                amigo = amigos[int(parte) - 1]
                if not any(s == amigo for s in selecionados):
                    selecionados.append(amigo)

            if not selecionados:
                raise Exception("Nenhum amigo selecionado para o grupo.")

            participantes: list[Usuario] = [self.__usuarioAtivo] + selecionados
            hora_atual = datetime.now().time().replace(microsecond=0)
            self.__sessaoInicioGrupo.iniciarPercursoGrupo(trilha, hora_atual, participantes)
            print(
                f"\nPercurso em grupo ({len(participantes)} participantes) iniciado na trilha '{trilha.nome}'!\n"
            )
        except Exception as e:
            print(f"\nErro ao iniciar percurso em grupo: {e}\n")

    def finalizarPercurso(self) -> None:
        percurso = self.__usuarioAtivo.percursoAtivo
        if percurso is None:
            print("\nVocê não tem nenhum percurso em andamento no momento.\n")
            return

        print(f"\n=== FINALIZANDO PERCURSO: {percurso.trilha.nome} ===")

        try:
            tempo_str = input("Quanto tempo você levou? (Formato: 'horas minutos'): ").strip()
            partes_tempo = tempo_str.split()
            if len(partes_tempo) != 2:
                raise Exception(
                    "Formato de tempo inválido. Digite horas e minutos separados por espaço (ex: 2 30)."
                )
            try:
                h, m = int(partes_tempo[0]), int(partes_tempo[1])
            except ValueError:
                raise Exception("Horas e minutos devem ser números inteiros.")
            if h < 0 or not (0 <= m < 60):
                raise Exception("Tempo inválido: informe horas >= 0 e minutos entre 0 e 59.")
            duracao = time(h, m, 0)

            dif_str = input("Qual dificuldade você sentiu na trilha? (1 a 10): ").strip()
            try:
                dificuldade = int(dif_str)
            except ValueError:
                raise Exception("A dificuldade percebida deve ser um número inteiro entre 1 e 10.")

            if isinstance(percurso, RegistroGrupo):
                notas: list[float] = []
                for membro in percurso.usuarios:
                    nota_str = input(
                        f"Qual nota '{membro.nome}' dá para a trilha? (0.0 a 5.0): "
                    ).strip()
                    try:
                        notas.append(float(nota_str))
                    except ValueError:
                        raise Exception(
                            f"Nota inválida informada para '{membro.nome}'. Digite um número entre 0.0 e 5.0."
                        )

                self.__sessaoFinalizarGrupo.finalizarPercursoGrupo(
                    self.__usuarioAtivo, duracao, notas, dificuldade
                )
                print(
                    f"\nPercurso em grupo ({percurso.qtdUsuarios} participantes) finalizado e registrado com sucesso!\n"
                )
            elif isinstance(percurso, RegistroIndividual):
                nota_str = input("Qual nota você dá para a trilha? (0.0 a 5.0): ").strip()
                try:
                    nota = float(nota_str)
                except ValueError:
                    raise Exception("Nota inválida. Digite um número decimal entre 0.0 e 5.0.")

                self.__sessaoFinalizarInd.finalizarPercurso(
                    self.__usuarioAtivo, duracao, nota, dificuldade
                )
                print("\nPercurso individual finalizado e registrado com sucesso!\n")
            else:
                raise Exception("Tipo de registro de percurso desconhecido.")
        except Exception as e:
            print(f"\nErro ao finalizar percurso: {e}\n")

    def cadastrarTrilha(self) -> None:
        print("Para cadastrar sua trilha, preencha os campos ou digite 'sair' para cancelar:")
        nome = input("Nome da trilha: ").strip().replace("\x00", "")
        if nome.lower() == "sair" or not nome:
            print("Cadastro cancelado.")
            return

        inicio = input("Local de início: ").strip().replace("\x00", "")
        if inicio.lower() == "sair" or not inicio:
            print("Cadastro cancelado.")
            return

        fim = input("Local de fim: ").strip().replace("\x00", "")
        if fim.lower() == "sair" or not fim:
            print("Cadastro cancelado.")
            return

        try:
            try:
                dif = int(input("Dificuldade (1 a 10): ").strip())
                comp = float(input("Comprimento (km): ").strip())
                alturaMin = int(input("Menor altitude (m): ").strip())
                alturaMax = int(input("Maior altitude (m): ").strip())
                partes_duracao = (
                    input("Tempo médio de duração ('horas minutos', ex: 2 15): ")
                    .strip()
                    .split()
                )
                if len(partes_duracao) != 2:
                    raise Exception(
                        "Formato de duração inválido. Informe horas e minutos separados por espaço (ex: 2 15)."
                    )
                horas, minutos = int(partes_duracao[0]), int(partes_duracao[1])
            except ValueError:
                raise Exception(
                    "Valores numéricos inválidos informados nos dados da trilha."
                )

            self.__sessaoCadastroTrilha.criarTrilha(
                nome=nome,
                inicio=inicio,
                fim=fim,
                dif=dif,
                comp=comp,
                alturaMin=alturaMin,
                alturaMax=alturaMax,
                horas=horas,
                minutos=minutos,
                usuario=self.__usuarioAtivo,
            )
            print("\nTrilha cadastrada com sucesso! Aguardando aprovação de um moderador.\n")
        except Exception as e:
            print(f"\nErro no cadastro da trilha: {e}\n")

    def excluirConta(self) -> bool:
        print("\n=== EXCLUIR CONTA ===")
        print("ATENÇÃO: Esta ação é irreversível e removerá seus dados do sistema.")
        confirmacao = input(
            "Digite 'CONFIRMAR' para prosseguir (ou qualquer tecla para cancelar): "
        ).strip()
        if confirmacao != "CONFIRMAR":
            print("Operação cancelada.\n")
            return False

        senha = input("Digite sua senha atual para confirmar a exclusão: ").strip()
        try:
            self.__sessaoExcluirConta.excluirConta(self.__usuarioAtivo, senha)
            print(f"\nConta '{self.__usuarioAtivo.nome}' excluída permanentemente.\n")
            return True
        except Exception as e:
            print(f"\nErro ao excluir conta: {e}\n")
            return False

    @staticmethod
    def __lerIntOpcional(prompt: str) -> Optional[int]:
        val = input(prompt).strip()
        if not val:
            return None
        try:
            return int(val)
        except ValueError:
            raise Exception(f"Valor inteiro inválido: '{val}'.")

    @staticmethod
    def __lerFloatOpcional(prompt: str) -> Optional[float]:
        val = input(prompt).strip()
        if not val:
            return None
        try:
            return float(val)
        except ValueError:
            raise Exception(f"Valor decimal inválido: '{val}'.")