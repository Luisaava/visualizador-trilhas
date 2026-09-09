from datetime import date,time
from .usuarios import Usuario, Moderador

trilhas: dict[str,Trilha] = {}

class Trilha:
    nome: str
    localInicio: str
    localFim: str
    dificuldade: int
    avaliacao: float
    variacaoAltitude: int
    duracaoMedia: time
    criador: Usuario
    apvoradaPor: Moderador

    def __init__(self, nome:str, inicio: str, fim: str, dif: int, alturaMin: int, alturaMax: int, tempoMedio: time, usuario: Usuario):
        self.nome = nome
        self.localInicio = inicio
        self.localFim = fim
        self.dificuldade = dif
        self.avaliacao = 0.0
        self.variacaoAltitude = alturaMax - alturaMin
        self.duracaoMedia = tempoMedio
        self.criador = usuario
        trilhas[self.nome] = self



class Registro:
    trilha: Trilha
    data: date
    duracao: time
    nota: float

class RegistroIndividual(Registro):
    usuario: Usuario

class RegistroGrupo(Registro):
    grupo: list[Usuario]
    quantidadeMembros: int