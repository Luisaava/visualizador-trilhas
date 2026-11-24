from __future__ import annotations
from typing import Optional


class Conquista:
    def __init__(
        self,
        nome: str,
        descricao: str,
        porcentagemDesbloqueio: float = 0.0,
        id: Optional[int] = None,
    ):
        self.__id: Optional[int] = id
        self.__nome: str = nome
        self.__descricao: str = descricao
        self.__porcentagemDesbloqueio: float = porcentagemDesbloqueio

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
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        self.__descricao = valor

    @property
    def porcentagemDesbloqueio(self) -> float:
        return self.__porcentagemDesbloqueio

    @porcentagemDesbloqueio.setter
    def porcentagemDesbloqueio(self, valor: float) -> None:
        self.__porcentagemDesbloqueio = valor

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Conquista):
            return False
        if self.__id is not None and other.id is not None:
            return self.__id == other.id
        return self.__nome == other.nome

    def __str__(self) -> str:
        return f"{self.__nome}: {self.__descricao} ({self.__porcentagemDesbloqueio:.1f}% dos usuários)"
