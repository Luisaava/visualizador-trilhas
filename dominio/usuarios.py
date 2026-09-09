from datetime import date,datetime, time
from .trilhas import Registro, Trilha, trilhas
u = Usuario('nome','senha')
v = Usuario('nome2','senha2')
usuarios: dict[str, Usuario] = {u.nome : u, v.nome : v}

class Usuario:
    nome: str
    senha: str
    dataEntrada: date
    amigos: list[Usuario]
    conquistas: list[Conquista]
    trilhasConcluidas: list[Registro]
    pedidosAmizade: dict[str, Usuario]

    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
        self.dataEntrada = datetime.now()
        self.amigos = []
        self.conquistas = []
        self.trilhasConcluidas = []
        self.pedidosAmizade = {}
        usuarios[self.nome] = self

    def criarTrilha(self, nome: str, inicio: str, fim: str, dif: int, alturaMin: int, alturaMax: int, tempoMedio: time):
         Trilha(nome, inicio, fim, dif, alturaMin, alturaMax, tempoMedio, self)
    
    def adicionarAmigo(self, u: Usuario):
        u.pedidosAmizade[self.nome] = self
        print(f'Pedido de amizade enviado para {u.nome}')
    
    def aceitarPedido(self, u: Usuario): 
        self.amigos.append(u)
        self.pedidosAmizade.pop(u.nome)
        print(f'Pedido de amizade de {u.nome} aceito.')



class Moderador(Usuario):
    trilhasAprovacao: dict[str,Trilha] = {}

    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)
    
    def aprovarTrilha(self, nome:str) -> bool:
        if not trilhas[nome]:
            trilhas[nome] = Moderador.trilhasAprovacao.pop(nome)
            return True
        print(f'Erro: Trilha com nome {nome} já existente.')
        return False



class Conquista:
    pass