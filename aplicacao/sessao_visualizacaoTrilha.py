from __future__ import annotations
from typing import Optional
from dominio.trilhas import Trilha
from servicos_tecnicos.mapeador import Mapeador


class SessaoVisualizacaoTrilha:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def listarTrilhasAprovadas(self) -> list[Trilha]:
        trilhas = self.__mapeador.getTrilhasAprovadas()
        if not trilhas:
            raise Exception("Nenhuma trilha aprovada disponível no momento.")
        return trilhas

    def visualizarTrilha(self, nome: str) -> Trilha:
        if not nome or not nome.strip():
            raise Exception("Informe o nome da trilha que deseja visualizar.")

        trilha = self.__mapeador.getTrilhaPorNome(nome.strip())
        if trilha is None or trilha.aprovadaPor is None:
            raise Exception(
                f"Trilha '{nome.strip()}' não encontrada ou ainda pendente de aprovação."
            )
        return trilha