from __future__ import annotations
from typing import Optional
from dominio.usuarios import Usuario
from servicos_tecnicos.mapeador import Mapeador


class SessaoCadastroUsuario:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def criarUsuario(self, nome: str, senha: str) -> Usuario:
        nome_limpo = nome.strip() if nome else ""
        senha_limpa = senha.strip() if senha else ""

        if not nome_limpo:
            raise Exception("O nome de usuário não pode estar vazio.")
        if not senha_limpa:
            raise Exception("A senha não pode estar vazia.")
        if len(senha_limpa) < 4:
            raise Exception("A senha deve conter pelo menos 4 caracteres.")

        if self.__mapeador.getUsuarioPorNome(nome_limpo) is not None:
            raise Exception(f"O nome de usuário '{nome_limpo}' já está em uso.")

        novo_usuario = Usuario(nome=nome_limpo, senha=senha_limpa)
        return self.__mapeador.salvarUsuario(novo_usuario)