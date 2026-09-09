from dominio.usuarios import Usuario

class InterfaceUsuario:
    usuarioAtivo: Usuario
    def __init__(self, u: Usuario):
        self.usuarioAtivo = u
        self.exibirInterface()
    
    def exibirInterface(self):
        print(f'Bem vindo, {self.usuarioAtivo.nome}.\n')
        print("""Opções:\n
        1 - Exibir pefil\n
        2 - Exibir amigos\n
        3 - Enviar pedido de amizade\n
        4 - Exibir e aceitar pedidos de amizade\n
        5 - Criar trilha\n
        6 - Realizar trilha individual\n
        7 - Realizar trilha em grupo\n
        8 - Postar conclusão de trilha\n
        0 - Sair\n""")
        while True:
            op: str = input("Digite um número para escolher uma opção: ")
            match(op):
                case '1':
                    self.exibirPerfil()
                case '2':
                    self.exibirAmigos()
                case '3':
                    pass
                case '4':
                    pass
                case '5':
                    pass
                case '6':
                    pass
                case '7':
                    pass
                case '0':
                    break
                case _:
                    print("Opção inválida.\n")

    def exibirPerfil(self):
        print(self.usuarioAtivo)

    def exibirAmigos(self):
        if len(self.usuarioAtivo.amigos == 0): print("Você não possui nenhum amigo."); return
        for amigo in self.usuarioAtivo.amigos: print(amigo.nome)
        print(f'Você possui {len(self.usuarioAtivo.amigos)} amigos.')
    
    def enviarPedido(self):
        pass

