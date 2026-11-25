#PROXIMA ITERACAO
from servicos_tecnicos.mapeador import Mapeador
from dominio.trilhas import Trilha
from dominio.usuarios import Moderador, Usuario
from datetime import time

class SessaoCadastroTrilha:
    def __init__(self):
        self.mapeador = Mapeador.getInstancia()
    def criarTrilha(self, nome: str, inicio: str, fim: str, dif: int, comp: float, alturaMin: int, alturaMax: int, horas: int, minutos: int, usuario: Usuario):
        self.trilhaInexistente(nome)
        self.inicioEFimDiferentes(inicio, fim)
        self.variacaoAltitudeValida(alturaMin, alturaMax)
        self.dificuldadeValida(dif)
        self.comprimentoValido(comp)
        self.tempoValido(horas, minutos)
        t = Trilha(nome, inicio, fim, dif, comp, alturaMin, alturaMax, time(horas, minutos, 0), usuario)
        Moderador.trilhasAprovacao[nome] = t
        # mandar pra moderador
    def trilhaInexistente(self, nome: str) -> None:
        if self.mapeador.getTrilha(nome) is not None:
            raise Exception("Trilha com nome já existente. Tente novamente.")
    def inicioEFimDiferentes(self, inicio:str, fim:str):
        if inicio == fim:
            raise Exception("Trilha com início e fim iguais. Tente novamente.")
    def variacaoAltitudeValida(self, alturaMin: int, alturaMax: int):
        if alturaMax < alturaMin:
            raise Exception("A altura máxima não pode ser menor do que a mínima. Tente novamente.")
    def dificuldadeValida(self, dif: int):
        if dif < 1 or dif > 10:
            raise Exception("O valor deve ser entre 1 e 10. Tente novamente.")
    def comprimentoValido(self, comp: float):
        if comp < 0.1:
            raise Exception("O valor deve ser positivo e maior que 0.1. Tente novamente.")
    def tempoValido(self, horas: int, minutos: int):
        if horas < 0:
            raise Exception("Horas não podem ser negativas. Tente novamente.")
        if minutos < 0 or minutos >= 60:
            raise Exception("Minutos não podem ser negativos e nem exceder o valor 60. Tente novamente.")