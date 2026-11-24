from __future__ import annotations
from typing import Optional
from dominio.usuarios import Moderador, Usuario
from servicos_tecnicos.mapeador import Mapeador


class SessaoExcluirConta:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def validarSenha(self, usuario: Usuario, senha: str) -> bool:
        if usuario is None:
            raise Exception("Nenhum usuário autenticado para validar a senha.")
        if not senha:
            raise Exception("Informe a senha para confirmar a exclusão da conta.")
        if usuario.senha != senha:
            raise Exception("Senha incorreta. Exclusão de conta cancelada.")
        return True

    def excluirConta(self, usuario: Usuario, senha: str) -> None:
        if isinstance(usuario, Moderador):
            raise Exception("Contas de moderador não podem ser excluídas por esta interface.")
        if usuario.id is None:
            raise Exception("Usuário não identificado no banco de dados.")

        self.validarSenha(usuario, senha)

        if usuario.percursoAtivo is not None:
            raise Exception("Finalize seu percurso ativo antes de excluir a conta.")

        removido = self.__mapeador.removerUsuario(usuario.id)
        if not removido:
            raise Exception("Não foi possível excluir a conta no banco de dados.")