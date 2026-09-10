from __future__ import annotations
from datetime import date, time
from typing import Optional


class Usuario:
    nome: str
    senha: str
    dataEntrada: date
    amigos: list[str]
    pedidosAmizade: list[str]

    def __init__(
        self,
        nome: str,
        senha: str,
        dataEntrada: Optional[str] = None,
        amigos: Optional[list[str]] = None,
        pedidosAmizade: Optional[list[str]] = None,
    ):
        self.nome = nome
        self.senha = senha
        self.dataEntrada = date.fromisoformat(dataEntrada) if dataEntrada else date.today()
        self.amigos = amigos if amigos is not None else []
        self.pedidosAmizade = pedidosAmizade if pedidosAmizade is not None else []
        self.conquistas = []
        self.trilhasConcluidas = []

    def __str__(self) -> str:
        return f"{self.nome} (membro desde {self.dataEntrada})"

    def adicionarAmigo(self, destinatario: Usuario) -> tuple[bool, str]:
        if destinatario.nome == self.nome:
            return False, "Você não pode enviar pedido para si mesmo."
        if destinatario.nome in self.amigos:
            return False, f"Você já é amigo de {destinatario.nome}."
        if self.nome in destinatario.pedidosAmizade:
            return False, f"Pedido já enviado para {destinatario.nome}."

        destinatario.pedidosAmizade.append(self.nome)
        return True, f"Pedido de amizade enviado para {destinatario.nome}."

    def aceitarPedido(self, remetente: Usuario) -> tuple[bool, str]:
        # if remetente.nome not in self.pedidosAmizade:
        #     return False, f"Não há pedido pendente de {remetente.nome}."

        self.pedidosAmizade.remove(remetente.nome)
        self.amigos.append(remetente.nome)
        remetente.amigos.append(self.nome)
        return True, f"Pedido de amizade de {remetente.nome} aceito."

    def recusarPedido(self, nome_remetente: str) -> tuple[bool, str]:
        if nome_remetente in self.pedidosAmizade:
            self.pedidosAmizade.remove(nome_remetente)
            return True, f"Pedido de {nome_remetente} recusado."
        # return False, "Pedido não encontrado."

    # def criarTrilha(self, nome: str, inicio: str, fim: str, dif: int, alturaMin: int, alturaMax: int, tempoMedio: time):
    #     # Trilha(nome, inicio, fim, dif, alturaMin, alturaMax, tempoMedio, self)
    #     pass

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "senha": self.senha,
            "dataEntrada": self.dataEntrada.isoformat(),
            "amigos": self.amigos,
            "pedidosAmizade": self.pedidosAmizade,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> Usuario:
        return cls(
            nome=dados["nome"],
            senha=dados["senha"],
            dataEntrada=dados.get("dataEntrada"),
            amigos=dados.get("amigos", []),
            pedidosAmizade=dados.get("pedidosAmizade", []),
        )


class Moderador(Usuario):
    trilhasAprovacao: dict = {}

    def __init__(self, nome: str = "moderador", senha: str = "123"):
        super().__init__(nome=nome, senha=senha)

    def aprovarTrilha(self, nome: str, trilhas_globais: dict) -> tuple[bool, str]:
        if nome not in trilhas_globais:
            if nome in Moderador.trilhasAprovacao:
                trilhas_globais[nome] = Moderador.trilhasAprovacao.pop(nome)
                return True, f"Trilha '{nome}' aprovada com sucesso."
            return False, f"Trilha '{nome}' não está na fila de aprovação."
        return False, f"Erro: Trilha com nome '{nome}' já existente."