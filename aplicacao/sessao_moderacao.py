from __future__ import annotations
from typing import Optional
from dominio.usuarios import Usuario, Moderador
from dominio.trilhas import Trilha
from servicos_tecnicos.mapeador import Mapeador


class SessaoAprovarTrilha:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def listarUsuarios(self) -> list[Usuario]:
        return self.__mapeador.getTodosUsuarios()

    def listarTrilhasPendentes(self) -> list[Trilha]:
        return self.__mapeador.getTrilhasPendentes()

    def definirAprovador(self, trilha: Trilha, moderador: Moderador) -> None:
        if not isinstance(moderador, Moderador):
            raise Exception("Apenas moderadores têm permissão para aprovar trilhas.")
        if trilha is None:
            raise Exception("Trilha não encontrada.")

        sucesso, msg = moderador.aprovarTrilha(trilha)
        if not sucesso:
            raise Exception(msg)

    def aprovarTrilha(self, moderador: Moderador, nome: str) -> None:
        if not nome or not nome.strip():
            raise Exception("Informe o nome da trilha a ser aprovada.")

        trilha = self.__mapeador.getTrilhaPorNome(nome.strip())
        if trilha is None:
            raise Exception(f"Trilha '{nome.strip()}' não encontrada.")

        self.definirAprovador(trilha, moderador)
        self.__mapeador.atualizarTrilha(trilha)

    def rejeitarTrilha(self, trilha: Trilha) -> None:
        if trilha is None or trilha.id is None:
            raise Exception("Trilha inválida ou não encontrada no banco de dados.")
        removida = self.__mapeador.removerTrilha(trilha.id)
        if not removida:
            raise Exception(f"Não foi possível remover a trilha '{trilha.nome}'.")