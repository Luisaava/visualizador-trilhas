from aplicacao.sessao_cadastroUsuario import SessaoCadastro
from aplicacao.sessao_login import SessaoLogin
from apresentacao.interface_usuario import InterfaceUsuario
from apresentacao.interface_moderador import InterfaceModerador
from servicos_tecnicos.persistencia import PersistenciaJSON


class InterfaceInicial:
    def __init__(
        self,
        sessao_cadastro: SessaoCadastro,
        sessao_login: SessaoLogin,
        persistencia: PersistenciaJSON,
    ):
        self.sessao_cadastro = sessao_cadastro
        self.sessao_login = sessao_login
        self.persistencia = persistencia

    def executar(self):
        while True:
            print("\n==============================")
            print("     SISTEMA DE TRILHAS       ")
            print("==============================")
            print("1 - Entrar (Login)")
            print("2 - Criar Conta (Cadastro)")
            print("0 - Sair")

            opcao = input("Escolha uma opção: ").strip()

            match opcao:
                case "1":
                    self.tela_login()
                case "2":
                    self.tela_cadastro()
                case "0":
                    print("tchau tchau!!")
                    break
                case _:
                    print("Opção inválida.\n")

    def tela_login(self):
        nome = input("Digite o nome de usuário: ").strip()
        senha = input("Digite a senha: ").strip()

        sucesso, tipo, usuario = self.sessao_login.autenticar(nome, senha)

        if not sucesso:
            print("Erro: Usuário ou senha incorretos.\n")
            return

        if tipo == "MODERADOR":
            tela_mod = InterfaceModerador(self.persistencia)
            tela_mod.exibir_painel()
        elif tipo == "USUARIO" and usuario:
            InterfaceUsuario(usuario, self.persistencia)

    def tela_cadastro(self):
        print("\n--- CADASTRO DE CONTA ---")
        nome = input("Escolha um nome de usuário: ").strip()
        senha = input("Escolha uma senha: ").strip()

        sucesso, _, msg = self.sessao_cadastro.criar_usuario(nome, senha)
        print(msg)