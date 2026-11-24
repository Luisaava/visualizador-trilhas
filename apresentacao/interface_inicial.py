from __future__ import annotations
from typing import Optional
from aplicacao.sessao_cadastroUsuario import SessaoCadastroUsuario
from aplicacao.sessao_login import SessaoLogin
from apresentacao.interface_usuario import InterfaceUsuario
from apresentacao.interface_moderador import InterfaceModerador
from dominio.usuarios import Moderador


class InterfaceInicial:
    def __init__(
        self,
        sessao_cadastro: Optional[SessaoCadastroUsuario] = None,
        sessao_login: Optional[SessaoLogin] = None,
    ):
        self.__sessao_cadastro: SessaoCadastroUsuario = (
            sessao_cadastro if sessao_cadastro is not None else SessaoCadastroUsuario()
        )
        self.__sessao_login: SessaoLogin = (
            sessao_login if sessao_login is not None else SessaoLogin()
        )

    def executar(self) -> None:
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
                    self.telaLogin()
                case "2":
                    self.telaCadastro()
                case "0":
                    print("Até logo!")
                    break
                case _:
                    print("Opção inválida.\n")

    def telaLogin(self) -> None:
        nome = input("Digite o nome de usuário: ").strip()
        senha = input("Digite a senha: ").strip()

        try:
            usuario = self.__sessao_login.autenticar(nome, senha)
            if isinstance(usuario, Moderador):
                tela_mod = InterfaceModerador(usuario)
                tela_mod.exibirPainel()
            else:
                InterfaceUsuario(usuario)
        except Exception as e:
            print(f"\nErro ao realizar login: {e}\n")

    def telaCadastro(self) -> None:
        print("\n--- CADASTRO DE CONTA ---")
        nome = input("Escolha um nome de usuário: ").strip()
        senha = input("Escolha uma senha: ").strip()

        try:
            usuario = self.__sessao_cadastro.criarUsuario(nome, senha)
            print(f"\nUsuário '{usuario.nome}' cadastrado com sucesso!\n")
        except Exception as e:
            print(f"\nErro no cadastro: {e}\n")