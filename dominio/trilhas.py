#usar builder como padrão de projeto

from datetime import date,time
from .usuarios import Usuario, Moderador
from abc import ABC

trilhas: dict[str,Trilha] = {}

class Trilha:
    _nome: str
    _localInicio: str
    _localFim: str
    _dificuldade: int
    _comprimento: float
    _avaliacao: float = 0.0
    _variacaoAltitude: int
    _duracaoMedia: time
    _criador: Usuario
    _apvoradaPor: Moderador

    def __init__(self, nome:str, inicio: str, fim: str, dif: int, comprimento: float, alturaMin: int, alturaMax: int, tempoMedio: time, usuario: Usuario):
        self.nome = nome
        self.localInicio = inicio
        self.localFim = fim
        self.dificuldade = dif
        self.comprimento = comprimento
        self.variacaoAltitude = alturaMax - alturaMin
        self.duracaoMedia = tempoMedio
        self.criador = usuario
    def setAprovada(moderador):
        _apvoradaPor = moderador
class Registro(ABC):
    _trilha: Trilha
    _data: date
    _duracao: time
    _nota: float

class RegistroIndividual(Registro):
    _usuario: Usuario

class RegistroGrupo(Registro):
    _grupo: list[Usuario]
    _quantidadeMembros: int