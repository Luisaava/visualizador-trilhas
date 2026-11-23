#PROXIMA ITERACAO
from dominio.trilhas import Trilha, trilhas
from dominio.usuarios import Moderador, Usuario
from datetime import time

class SessaoCadastroTrilha:
    def __init__(self):
        pass
    def criarTrilha(self, nome: str, inicio: str, fim, dif: int, comp: float, alturaMin: int, alturaMax: int, horas: int, minutos: int, usuario: Usuario):
        self.trilhaInexistente(nome)
        self.inicioEFimDiferentes(inicio, fim)
        self.variacaoAltitudeValida(alturaMin, alturaMax)
        self.dificuldadeValida(dif)
        self.comprimentoValido(comp)
        self.tempoValido(horas, minutos)
        t = Trilha(nome, inicio, fim, dif, comp, alturaMin, alturaMax, time(horas, minutos, 0), usuario)
        Moderador.trilhasAprovacao[nome] = t
        # mandar pra moderador
    def trilhaInexistente(self, nome):
        if trilhas.get(nome, None) is not None:
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
        if comp < 0.0 or comp < 0.1:
            raise Exception("O valor deve ser positivo e maior que 0.1. Tente novamente.")
    def tempoValido(self, horas: int, minutos: int):
        if horas < 0:
            raise Exception("Horas não podem ser negativas. Tente novamente.")
        if minutos < 0 or minutos >= 60:
            raise Exception("Minutos não podem ser negativos e nem exceder o valor 60. Tente novamente.")
# while True:
#     nome = input("Digite o nome da sua trilha: ").strip().replace("\x00","")
#     if nome.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     if nome == "":
#         print("O nome não pode ser vazio, tente novamente.")
#         continue
#     break
# while True:
#     inicio = input("Digite o local do início da sua trilha: ").strip().replace("\x00","")
#     if inicio.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     if inicio == "":
#         print("O local do início não pode ser vazio, tente novamente.")
#         continue
#     break
# while True:
#     fim = input("Digite o local do fim da sua trilha: ").strip().replace("\x00","")
#     if fim.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     if fim == "":
#         print("O local do fim não pode ser vazio, tente novamente.")
#         continue
#     if fim.lower() == inicio.lower():
#         print("O início não pode ser igual ao fim.")
#         continue
#     break
# while True:
#     dif = input("Digite a dificuldade da sua trilha (de 1 a 10): ").strip()
#     if dif.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     try:
#         dif = int(dif)
#         if dif < 1 or dif > 10:
#             print("O valor deve ser entre 1 e 10.")
#             continue
#     except ValueError:
#         print("Valor inválido. Tente novamente.")
#         continue
#     break
# while True:
#     comp = input("Digite o comprimento da sua trilha: ").strip()
#     if comp.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     try:
#         comp = float(comp)
#         if comp < 0.0 or comp < 0.1:
#             print("O valor deve ser positivo e maior que 0.1.")
#             continue
#     except ValueError:
#         print("Valor inválido. Tente novamente.")
#         continue
#     break
# while True:
#     alturaMin = input("Digite o ponto de menor altitude da sua trilha: ").strip()
#     if alturaMin.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     try:
#         alturaMin = int(alturaMin)
#     except ValueError:
#         print("Valor inválido. Tente novamente.")
#         continue
#     break
#
# while True:
#     alturaMax = input("Digite o ponto de maior altitude da sua trilha: ").strip()
#     if alturaMax.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     try:
#         alturaMax = int(alturaMax)
#         if alturaMax < alturaMin:
#             print("A altura máxima não pode ser menor do que a mínima. Tente novamente.")
#             continue
#     except ValueError:
#         print("Valor inválido. Tente novamente.")
#         continue
#     break
# while True:
#     tempoMedio = input("Digite o tempo médio de duração da sua trilha, no formato 'horas minutos': ").strip()
#     if tempoMedio.lower() == "sair":
#         print("Saindo do cadastro.")
#         return
#     try:
#         horas, minutos = tempoMedio.split()
#     except ValueError:
#         print("Não há valores suficientes para preencher os dados.")
#         continue
#     try:
#         horas = int(horas)
#         if horas < 0:
#             print("Horas não podem ser negativas. Tente novamente.")
#             continue
#         minutos = int(minutos)
#         if minutos < 0 or minutos >= 60:
#             print("Minutos não podem ser negativos e nem exceder o valor 60. Tente novamente.")
#             continue
#     except ValueError:
#         print("Valor inválido. Tente novamente.")
#         continue
#     tempoMedio = time(horas, minutos, 0)
#     break