from __future__ import annotations
from datetime import time
from typing import Optional
from dominio.trilhas import Trilha
from dominio.usuarios import Moderador, Usuario
from servicos_tecnicos.mapeador import Mapeador


class SessaoCadastroTrilha:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def trilhaInexistente(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise Exception("O nome da trilha não pode estar vazio.")
        if self.__mapeador.getTrilhaPorNome(nome.strip()) is not None:
            raise Exception(f"Já existe uma trilha cadastrada com o nome '{nome.strip()}'.")

    def inicioEFimDiferentes(self, inicio: str, fim: str) -> None:
        if not inicio or not inicio.strip():
            raise Exception("O local de início da trilha deve ser informado.")
        if not fim or not fim.strip():
            raise Exception("O local de fim da trilha deve ser informado.")
        if inicio.strip().lower() == fim.strip().lower():
            raise Exception("O local de início e o local de fim da trilha devem ser diferentes.")

    def variacaoAltitudeValida(self, alturaMin: int, alturaMax: int) -> None:
        if alturaMin < 0 or alturaMax < 0:
            raise Exception("As altitudes mínima e máxima não podem ser negativas.")
        if alturaMax < alturaMin:
            raise Exception("A altitude máxima deve ser maior ou igual à altitude mínima.")

    def dificuldadeValida(self, dif: int) -> None:
        if dif < 1 or dif > 10:
            raise Exception("A dificuldade da trilha deve ser um número inteiro entre 1 e 10.")

    def comprimentoValido(self, comp: float) -> None:
        if comp <= 0:
            raise Exception("O comprimento da trilha deve ser maior que zero.")

    def tempoValido(self, horas: int, minutos: int) -> None:
        if horas < 0 or minutos < 0 or minutos >= 60:
            raise Exception("Tempo inválido: informe horas >= 0 e minutos entre 0 e 59.")
        if horas == 0 and minutos == 0:
            raise Exception("A duração média da trilha deve ser maior que zero.")

    def criarTrilha(
        self,
        nome: str,
        inicio: str,
        fim: str,
        dif: int,
        comp: float,
        alturaMin: int,
        alturaMax: int,
        horas: int,
        minutos: int,
        usuario: Usuario,
    ) -> None:
        if usuario is None:
            raise Exception("É necessário estar autenticado para cadastrar uma trilha.")

        self.trilhaInexistente(nome)
        self.inicioEFimDiferentes(inicio, fim)
        self.variacaoAltitudeValida(alturaMin, alturaMax)
        self.dificuldadeValida(dif)
        self.comprimentoValido(comp)
        self.tempoValido(horas, minutos)

        variacao_altitude = alturaMax - alturaMin
        duracao_media = time(hour=horas, minute=minutos)
        aprovador = usuario if isinstance(usuario, Moderador) else None

        nova_trilha = Trilha(
            nome=nome.strip(),
            localInicio=inicio.strip(),
            localFim=fim.strip(),
            comprimento=comp,
            dificuldade=dif,
            variacaoAltitude=variacao_altitude,
            duracaoMedia=duracao_media,
            criador=usuario,
            avaliacao=0.0,
            aprovadaPor=aprovador,
        )

        trilha_salva = self.__mapeador.salvarTrilha(nova_trilha)
        usuario.trilhasCriadas.append(trilha_salva)