from dominio.usuarios import Usuario
from servicos_tecnicos.persistencia import PersistenciaJSON
from datetime import time
from aplicacao.sessao_cadastroTrilha import SessaoCadastroTrilha
from aplicacao.sessao_visualizacaoTrilha import SessaoVisualizacaoTrilha ####

class InterfaceUsuario:
    usuarioAtivo: Usuario
    persistencia: PersistenciaJSON
    cadastro: SessaoCadastroTrilha

    def __init__(self, u: Usuario, persistencia: PersistenciaJSON):
        self.usuarioAtivo = u
        self.persistencia = persistencia
        self.visualizacao = None
        self.cadastro = None
        self.exibirInterface()
    
    def exibirInterface(self):
        while True:
            print(f'Bem vindo, {self.usuarioAtivo.nome}.\n')
            print("""Opções:\n
            1 - Exibir perfil\n
            2 - Exibir amigos\n
            3 - Enviar pedido de amizade\n
            4 - Exibir e aceitar pedidos de amizade\n
            5 - Visualizar e escolher trilhas\n
            6 - Cadastrar Trilha\n
            7 - Finalizar Percurso em andamento\n
            0 - Sair\n""")
            op: str = input("Digite um número para escolher uma opção: ")
            match(op):
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
                    self.cadastrarTrilha()
                case "7":
                    self.finalizarPercurso()
                case '0':
                    break
                case _:
                    print("Opção inválida.\n")

    def exibirPerfil(self):
        print(self.usuarioAtivo)

    def exibirAmigos(self):
        if len(self.usuarioAtivo.amigos) == 0:
            print("Você não possui nenhum amigo.")
            return

        for amigo in self.usuarioAtivo.amigos:
            print(f"- {amigo}")
        print(f"Você possui {len(self.usuarioAtivo.amigos)} amigo(s).")
    
    def enviarPedido(self):
        nome_alvo = input("Digite o nome do usuário: ").strip()
        todos = self.persistencia.carregar_todos()
        alvo = todos.get(nome_alvo)

        if not alvo:
            print(f"Usuário '{nome_alvo}' não encontrado.\n")
            return

        sucesso, msg = self.usuarioAtivo.adicionarAmigo(alvo)
        print(f"\n{msg}\n")

        if sucesso:
            todos[alvo.nome] = alvo
            self.persistencia.salvar_todos(todos)

    def gerenciarPedidos(self):
        todos = self.persistencia.carregar_todos()
        
        if self.usuarioAtivo.nome in todos:
            self.usuarioAtivo = todos[self.usuarioAtivo.nome]

        pedidos = list(self.usuarioAtivo.pedidosAmizade)

        if len(pedidos) == 0:
            print("Nenhum pedido pendente.\n")
            return

        for idx, remetente in enumerate(pedidos, start=1):
            print(f"{idx} - {remetente}")

        escolha = input("Digite o número do usuário: ").strip()

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(pedidos)):
            print("Opção inválida.\n")
            return

        nome_alvo = pedidos[int(escolha) - 1]
        remetente_obj = todos.get(nome_alvo)

        if not remetente_obj:
            print(f"Erro: Usuário '{nome_alvo}' não encontrado.")
            return

        print(f"\nDeseja aceitar o pedido de {nome_alvo}?")
        print("1 - Sim  2 - Não")
        acao = input("Escolha: ").strip()

        if acao == "1":
            sucesso, msg = self.usuarioAtivo.aceitarPedido(remetente_obj)
            print(f"\n{msg}\n")
            if sucesso:
                todos[self.usuarioAtivo.nome] = self.usuarioAtivo
                todos[remetente_obj.nome] = remetente_obj
                self.persistencia.salvar_todos(todos)

        elif acao == "2":
            sucesso, msg = self.usuarioAtivo.recusarPedido(nome_alvo)
            print(f"\n{msg}\n")
            if sucesso:
                todos[self.usuarioAtivo.nome] = self.usuarioAtivo
                self.persistencia.salvar_todos(todos)
        else:
            print("Operação cancelada.\n")
    
    def cadastrarTrilha(self):
        nome = inicio = fim = dif = comp = alturaMin = alturaMax = tempoMedio = usuario = None
        print("Para cadastrar sua trilha, preencha os campos conforme pedido, ou digite 'sair' para sair")
        while True:
            nome = input("Digite o nome da sua trilha: ").strip()
            if nome.lower() == "sair":
                print("Saindo do cadastro.")
                return
            if "\x00" in nome:
                print("O nome possui um caractere inválido, tente novamente.")
                continue
            if nome == "":
                print("O nome não pode ser vazio, tente novamente.")
                continue
            break
        while True:
            inicio = input("Digite o local do início da sua trilha: ").strip()
            if inicio.lower() == "sair":
                print("Saindo do cadastro.")
                return
            if "\x00" in inicio:
                print("O local do início possui um caractere inválido, tente novamente.")
                continue
            if inicio == "":
                print("O local do início não pode ser vazio, tente novamente.")
                continue
            break
        while True:
            fim = input("Digite o local do fim da sua trilha: ").strip()
            if fim.lower() == "sair":
                print("Saindo do cadastro.")
                return
            if "\x00" in fim:
                print("O local do fim possui um caractere inválido, tente novamente.")
                continue
            if fim == "":
                print("O local do fim não pode ser vazio, tente novamente.")
                continue
            if fim.lower() == inicio.lower():
                print("O início não pode ser igual ao fim.")
            break
        while True:
            dif = input("Digite a dificuldade da sua trilha (de 1 a 10): ").strip()
            if dif.lower() == "sair":
                print("Saindo do cadastro.")
                return
            try:
                dif = int(dif)
                if dif < 1 or dif > 10:
                    print("O valor deve ser entre 1 e 10.")
                    continue
            except ValueError:
                print("Valor inválido. Tente novamente.")
            break
        while True:
            comp = input("Digite o comprimento da sua trilha: ").strip()
            if comp.lower() == "sair":
                print("Saindo do cadastro.")
                return
            try:
                comp = float(comp)
                if comp < 0.0 or comp < 0.1:
                    print("O valor deve ser positivo e maior que 0.1.")
                    continue
            except ValueError:
                print("Valor inválido. Tente novamente.")
            break
        while True:
            alturaMin = input("Digite o ponto de menor altitude da sua trilha: ").strip()
            if alturaMin.lower() == "sair":
                print("Saindo do cadastro.")
                return
            try:
                alturaMin = int(alturaMin)
            except ValueError:
                print("Valor inválido. Tente novamente.")
            break

        while True:
            alturaMax = input("Digite o ponto de maior altitude da sua trilha: ").strip()
            if alturaMax.lower() == "sair":
                print("Saindo do cadastro.")
                return
            try:
                alturaMax = int(alturaMax)
                if alturaMax < alturaMin:
                    print("A altura máxima não pode ser menor do que a mínima. Tente novamente.")
                    continue
            except ValueError:
                print("Valor inválido. Tente novamente.")
            break
        while True:
            tempoMedio = input("Digite o tempo médio de duração da sua trilha, no formato 'horas minutos': ").strip()
            if tempoMedio.lower() == "sair":
                print("Saindo do cadastro.")
                return
            try:
                horas, minutos = tempoMedio.split()
            except ValueError:
                print("Não há valores suficientes para preencher os dados.")
                continue
            try:
                horas = int(horas)
                if horas < 0:
                    print("Horas não podem ser negativas. Tente novamente.")
                    continue
                minutos = int(minutos)
                if minutos < 0 or minutos >= 60:
                    print("Minutos não podem ser negativos e nem exceder o valor 60. Tente novamente.")
            except ValueError:
                print("Valor inválido. Tente novamente.")
            tempoMedio = time(horas, minutos, 0)
            break
        try:
            if not self.cadastro:
                self.cadastro = SessaoCadastroTrilha()
            self.cadastro.criarTrilha(nome,inicio,fim,dif,comp,alturaMin,alturaMax,tempoMedio,self.usuarioAtivo)
            print("TRILHA CADASTRADA COM SUCESSO!!!!")

        except Exception as e: ##isso aqui usei mais pra ver qq era o erro mas acredito q da pra tirar 
            print(f"\nOcorreu um erro no cadastro: {type(e).__name__} - {e}")
            import traceback
            traceback.print_exc()

    def visualizarTrilhas(self):
        if not self.visualizacao:
            self.visualizacao = SessaoVisualizacaoTrilha()
            
        trilha_escolhida = self.visualizacao.exibir_trilhas()
        
        if trilha_escolhida:
            resp = input(f"\nDeseja iniciar o percurso na trilha '{trilha_escolhida.nome}' agora? (s/n): ").strip().lower()
            if resp == 's':
                self.iniciarPercurso(trilha_escolhida)
        