#PROXIMA ITERACAO
from dominio.trilhas import Trilha, trilhas
from dominio.usuarios import Moderador
class SessaoCadastroTrilha:
    def __init__():
        pass
    def criarTrilha(self, nome:str, inicio: str, fim: str, dif: int, comp: float, alturaMin: int, alturaMax: int, tempoMedio: time, usuario: Usuario):
        if trilhas.get(nome, None):
            raise Exception
        t = Trilha(nome, inicio, fim, dif, comp, alturaMin, alturaMax, tempoMedio, usuario)
        Moderador.trilhasAprovacao[nome] = t
        # mandar pra moderador
