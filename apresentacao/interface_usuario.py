from dominio.usuarios import Usuario
from servicos_tecnicos.persistencia import PersistenciaJSON


class InterfaceUsuario:
    usuarioAtivo: Usuario
    persistencia: PersistenciaJSON

    def __init__(self, u: Usuario, persistencia: PersistenciaJSON):
        self.usuarioAtivo = u
        self.persistencia = persistencia
        self.exibirInterface()
    
    def exibirInterface(self):
        print(f'Bem vindo, {self.usuarioAtivo.nome}.\n')
        print("""Opções:\n
        1 - Exibir pefil\n
        2 - Exibir amigos\n
        3 - Enviar pedido de amizade\n
        4 - Exibir e aceitar pedidos de amizade\n
        0 - Sair\n""")
        while True:
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

