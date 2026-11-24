from __future__ import annotations
from typing import Optional
from dominio.usuarios import Usuario
from servicos_tecnicos.mapeador import Mapeador


class SessaoLogin:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def autenticar(self, nome: str, senha: str) -> Usuario:
        if not nome or not nome.strip():
            raise Exception("Informe o nome de usuário.")
        if not senha:
            raise Exception("Informe a senha.")

        usuario = self.__mapeador.getUsuarioPorNome(nome.strip())
        if usuario is None:
            raise Exception(f"Usuário '{nome.strip()}' não encontrado.")
        if usuario.senha != senha:
            raise Exception("Senha incorreta.")

        return usuario