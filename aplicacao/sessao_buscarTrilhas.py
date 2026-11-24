from __future__ import annotations
from datetime import time
from typing import Optional
from dominio.trilhas import Trilha
from servicos_tecnicos.mapeador import Mapeador


class SessaoBuscarTrilhas:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def filtrarPorLocal(
        self, trilhas: list[Trilha], inicio: str | None, fim: str | None
    ) -> list[Trilha]:
        resultado = trilhas
        if inicio and inicio.strip():
            resultado = [
                t for t in resultado if inicio.strip().lower() in t.localInicio.lower()
            ]
        if fim and fim.strip():
            resultado = [
                t for t in resultado if fim.strip().lower() in t.localFim.lower()
            ]
        return resultado

    def filtrarPorDificuldade(self, trilhas: list[Trilha], dificuldade: int) -> list[Trilha]:
        if dificuldade < 1 or dificuldade > 10:
            raise Exception("O filtro de dificuldade deve ser um número inteiro entre 1 e 10.")
        return [t for t in trilhas if t.dificuldade == dificuldade]

    def filtrarPorComprimento(
        self, trilhas: list[Trilha], comprimentoMax: float
    ) -> list[Trilha]:
        if comprimentoMax <= 0:
            raise Exception("O comprimento máximo deve ser maior que zero.")
        return [t for t in trilhas if t.comprimento <= comprimentoMax]

    def filtrarPorAvaliacao(self, trilhas: list[Trilha], avaliacaoMin: float) -> list[Trilha]:
        if avaliacaoMin < 0.0 or avaliacaoMin > 5.0:
            raise Exception("A avaliação mínima deve estar entre 0.0 e 5.0.")
        return [t for t in trilhas if t.avaliacao >= avaliacaoMin]

    def filtrarPorDuracao(self, trilhas: list[Trilha], duracaoMax: time) -> list[Trilha]:
        if duracaoMax == time(0, 0):
            raise Exception("A duração máxima deve ser maior que zero.")
        return [t for t in trilhas if t.duracaoMedia <= duracaoMax]

    def buscarTrilhas(
        self,
        nome: str | None = None,
        localInicio: str | None = None,
        localFim: str | None = None,
        dificuldade: int | None = None,
        comprimentoMax: float | None = None,
        avaliacaoMin: float | None = None,
        duracaoMax: time | None = None,
    ) -> list[Trilha]:
        trilhas = self.__mapeador.getTrilhasAprovadas()

        if nome and nome.strip():
            trilhas = [t for t in trilhas if nome.strip().lower() in t.nome.lower()]
        if (localInicio and localInicio.strip()) or (localFim and localFim.strip()):
            trilhas = self.filtrarPorLocal(trilhas, localInicio, localFim)
        if dificuldade is not None:
            trilhas = self.filtrarPorDificuldade(trilhas, dificuldade)
        if comprimentoMax is not None:
            trilhas = self.filtrarPorComprimento(trilhas, comprimentoMax)
        if avaliacaoMin is not None:
            trilhas = self.filtrarPorAvaliacao(trilhas, avaliacaoMin)
        if duracaoMax is not None:
            trilhas = self.filtrarPorDuracao(trilhas, duracaoMax)

        if not trilhas:
            raise Exception("Nenhuma trilha encontrada com os filtros informados.")

        return trilhas