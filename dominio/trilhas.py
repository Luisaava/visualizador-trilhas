from __future__ import annotations
from abc import ABC
from datetime import time
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dominio.usuarios import Usuario, Moderador


class Trilha:
    def __init__(
        self,
        nome: str,
        localInicio: str,
        localFim: str,
        comprimento: float,
        dificuldade: int,
        variacaoAltitude: int,
        duracaoMedia: time,
        criador: Usuario,
        avaliacao: float = 0.0,
        aprovadaPor: Optional[Moderador] = None,
        id: Optional[int] = None,
    ):
        self.__id: Optional[int] = id
        self.__nome: str = nome
        self.__localInicio: str = localInicio
        self.__localFim: str = localFim
        self.__comprimento: float = float(comprimento)
        self.__avaliacao: float = float(avaliacao)
        self.__dificuldade: int = int(dificuldade)
        self.__variacaoAltitude: int = int(variacaoAltitude)
        self.__duracaoMedia: time = duracaoMedia
        self.__criador: Usuario = criador
        self.__aprovadaPor: Optional[Moderador] = aprovadaPor

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @id.setter
    def id(self, valor: Optional[int]) -> None:
        self.__id = valor

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self.__nome = valor

    @property
    def localInicio(self) -> str:
        return self.__localInicio

    @localInicio.setter
    def localInicio(self, valor: str) -> None:
        self.__localInicio = valor

    @property
    def localFim(self) -> str:
        return self.__localFim

    @localFim.setter
    def localFim(self, valor: str) -> None:
        self.__localFim = valor

    @property
    def comprimento(self) -> float:
        return self.__comprimento

    @comprimento.setter
    def comprimento(self, valor: float) -> None:
        self.__comprimento = float(valor)

    @property
    def avaliacao(self) -> float:
        return self.__avaliacao

    @avaliacao.setter
    def avaliacao(self, valor: float) -> None:
        self.__avaliacao = float(valor)

    @property
    def dificuldade(self) -> int:
        return self.__dificuldade

    @dificuldade.setter
    def dificuldade(self, valor: int) -> None:
        self.__dificuldade = int(valor)

    @property
    def variacaoAltitude(self) -> int:
        return self.__variacaoAltitude

    @variacaoAltitude.setter
    def variacaoAltitude(self, valor: int) -> None:
        self.__variacaoAltitude = int(valor)

    @property
    def duracaoMedia(self) -> time:
        return self.__duracaoMedia

    @duracaoMedia.setter
    def duracaoMedia(self, valor: time) -> None:
        self.__duracaoMedia = valor

    @property
    def criador(self) -> Usuario:
        return self.__criador

    @criador.setter
    def criador(self, valor: Usuario) -> None:
        self.__criador = valor

    @property
    def aprovadaPor(self) -> Optional[Moderador]:
        return self.__aprovadaPor

    @aprovadaPor.setter
    def aprovadaPor(self, valor: Optional[Moderador]) -> None:
        self.__aprovadaPor = valor

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Trilha):
            return False
        if self.__id is not None and other.id is not None:
            return self.__id == other.id
        return self.__nome == other.nome

    def __str__(self) -> str:
        return (
            f"{self.__nome} ({self.__localInicio} -> {self.__localFim}) | "
            f"Dif: {self.__dificuldade}/10 | Dist: {self.__comprimento:.1f} km | "
            f"Avaliação: {self.__avaliacao:.1f}/5.0"
        )


class Registro(ABC):
    def __init__(
        self,
        trilha: Trilha,
        tempo: Optional[time] = None,
        avaliacao: Optional[float] = None,
        dificuldade: Optional[int] = None,
        id: Optional[int] = None,
    ):
        self.__id: Optional[int] = id
        self.__trilha: Trilha = trilha
        self.__tempo: Optional[time] = tempo
        self.__avaliacao: Optional[float] = float(avaliacao) if avaliacao is not None else None
        self.__dificuldade: Optional[int] = int(dificuldade) if dificuldade is not None else None

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @id.setter
    def id(self, valor: Optional[int]) -> None:
        self.__id = valor

    @property
    def trilha(self) -> Trilha:
        return self.__trilha

    @trilha.setter
    def trilha(self, valor: Trilha) -> None:
        self.__trilha = valor

    @property
    def tempo(self) -> Optional[time]:
        return self.__tempo

    @tempo.setter
    def tempo(self, valor: Optional[time]) -> None:
        self.__tempo = valor

    @property
    def avaliacao(self) -> Optional[float]:
        return self.__avaliacao

    @avaliacao.setter
    def avaliacao(self, valor: Optional[float]) -> None:
        self.__avaliacao = float(valor) if valor is not None else None

    @property
    def dificuldade(self) -> Optional[int]:
        return self.__dificuldade

    @dificuldade.setter
    def dificuldade(self, valor: Optional[int]) -> None:
        self.__dificuldade = int(valor) if valor is not None else None


class RegistroIndividual(Registro):
    def __init__(
        self,
        trilha: Trilha,
        usuario: Usuario,
        tempo: Optional[time] = None,
        avaliacao: Optional[float] = None,
        dificuldade: Optional[int] = None,
        id: Optional[int] = None,
    ):
        super().__init__(
            trilha=trilha,
            tempo=tempo,
            avaliacao=avaliacao,
            dificuldade=dificuldade,
            id=id,
        )
        self.__usuario: Usuario = usuario

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @usuario.setter
    def usuario(self, valor: Usuario) -> None:
        self.__usuario = valor


class RegistroGrupo(Registro):
    def __init__(
        self,
        trilha: Trilha,
        usuarios: list[Usuario],
        tempo: Optional[time] = None,
        avaliacao: Optional[float] = None,
        dificuldade: Optional[int] = None,
        id: Optional[int] = None,
    ):
        super().__init__(
            trilha=trilha,
            tempo=tempo,
            avaliacao=avaliacao,
            dificuldade=dificuldade,
            id=id,
        )
        self.__usuarios: list[Usuario] = list(usuarios)
        self.__qtdUsuarios: int = len(self.__usuarios)

    @property
    def usuarios(self) -> list[Usuario]:
        return self.__usuarios

    @usuarios.setter
    def usuarios(self, valor: list[Usuario]) -> None:
        self.__usuarios = list(valor)
        self.__qtdUsuarios = len(self.__usuarios)

    @property
    def qtdUsuarios(self) -> int:
        return self.__qtdUsuarios

    @qtdUsuarios.setter
    def qtdUsuarios(self, valor: int) -> None:
        self.__qtdUsuarios = valor
