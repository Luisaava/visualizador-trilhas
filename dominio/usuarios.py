from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING
from dominio.conquistas import Conquista

if TYPE_CHECKING:
    from dominio.trilhas import Registro, Trilha


class Usuario:
    def __init__(
        self,
        nome: str,
        senha: str,
        dataEntrada: Optional[date] = None,
        id: Optional[int] = None,
        percursoAtivo: Optional[Registro] = None,
        amigos: Optional[list[Usuario]] = None,
        pedidosAmizade: Optional[list[Usuario]] = None,
        trilhasConcluidas: Optional[list[Registro]] = None,
        trilhasCriadas: Optional[list[Trilha]] = None,
        conquistas: Optional[list[Conquista]] = None,
    ):
        self.__id: Optional[int] = id
        self.__nome: str = nome
        self.__senha: str = senha
        if isinstance(dataEntrada, str):
            self.__dataEntrada: date = date.fromisoformat(dataEntrada)
        else:
            self.__dataEntrada: date = dataEntrada if dataEntrada is not None else date.today()
        self.__percursoAtivo: Optional[Registro] = percursoAtivo
        self.__amigos: list[Usuario] = amigos if amigos is not None else []
        self.__pedidosAmizade: list[Usuario] = pedidosAmizade if pedidosAmizade is not None else []
        self.__trilhasConcluidas: list[Registro] = trilhasConcluidas if trilhasConcluidas is not None else []
        self.__trilhasCriadas: list[Trilha] = trilhasCriadas if trilhasCriadas is not None else []
        self.__conquistas: list[Conquista] = conquistas if conquistas is not None else []

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
    def senha(self) -> str:
        return self.__senha

    @senha.setter
    def senha(self, valor: str) -> None:
        self.__senha = valor

    @property
    def dataEntrada(self) -> date:
        return self.__dataEntrada

    @dataEntrada.setter
    def dataEntrada(self, valor: date) -> None:
        self.__dataEntrada = valor

    @property
    def percursoAtivo(self) -> Optional[Registro]:
        return self.__percursoAtivo

    @percursoAtivo.setter
    def percursoAtivo(self, valor: Optional[Registro]) -> None:
        self.__percursoAtivo = valor

    @property
    def amigos(self) -> list[Usuario]:
        return self.__amigos

    @amigos.setter
    def amigos(self, valor: list[Usuario]) -> None:
        self.__amigos = valor

    @property
    def pedidosAmizade(self) -> list[Usuario]:
        return self.__pedidosAmizade

    @pedidosAmizade.setter
    def pedidosAmizade(self, valor: list[Usuario]) -> None:
        self.__pedidosAmizade = valor

    @property
    def trilhasConcluidas(self) -> list[Registro]:
        return self.__trilhasConcluidas

    @trilhasConcluidas.setter
    def trilhasConcluidas(self, valor: list[Registro]) -> None:
        self.__trilhasConcluidas = valor

    @property
    def trilhasCriadas(self) -> list[Trilha]:
        return self.__trilhasCriadas

    @trilhasCriadas.setter
    def trilhasCriadas(self, valor: list[Trilha]) -> None:
        self.__trilhasCriadas = valor

    @property
    def conquistas(self) -> list[Conquista]:
        return self.__conquistas

    @conquistas.setter
    def conquistas(self, valor: list[Conquista]) -> None:
        self.__conquistas = valor

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Usuario):
            return False
        if self.__id is not None and other.id is not None:
            return self.__id == other.id
        return self.__nome == other.nome

    def __str__(self) -> str:
        return f"{self.__nome} (membro desde {self.__dataEntrada})"

    def adicionarAmigo(self, destinatario: Usuario) -> tuple[bool, str]:
        if destinatario == self:
            return False, "Você não pode enviar pedido de amizade para si mesmo."
        if any(a == destinatario for a in self.__amigos):
            return False, f"Você já é amigo de {destinatario.nome}."
        if any(p == self for p in destinatario.pedidosAmizade):
            return False, f"Pedido já enviado para {destinatario.nome}."
        if any(p == destinatario for p in self.__pedidosAmizade):
            return False, f"{destinatario.nome} já enviou um pedido para você. Aceite-o na lista de pedidos."

        destinatario.pedidosAmizade.append(self)
        return True, f"Pedido de amizade enviado para {destinatario.nome}."

    def aceitarPedido(self, remetente: Usuario) -> tuple[bool, str]:
        if not any(p == remetente for p in self.__pedidosAmizade):
            return False, f"Não há pedido pendente de {remetente.nome}."

        self.__pedidosAmizade = [p for p in self.__pedidosAmizade if p != remetente]
        if not any(a == remetente for a in self.__amigos):
            self.__amigos.append(remetente)
        if not any(a == self for a in remetente.amigos):
            remetente.amigos.append(self)
        return True, f"Pedido de amizade de {remetente.nome} aceito."

    def recusarPedido(self, remetente: Usuario) -> tuple[bool, str]:
        if not any(p == remetente for p in self.__pedidosAmizade):
            return False, f"Não há pedido pendente de {remetente.nome}."

        self.__pedidosAmizade = [p for p in self.__pedidosAmizade if p != remetente]
        return True, f"Pedido de amizade de {remetente.nome} recusado."

    def adicionarConquista(self, conquista: Conquista) -> bool:
        if not any(c == conquista for c in self.__conquistas):
            self.__conquistas.append(conquista)
            return True
        return False


class Moderador(Usuario):
    def __init__(
        self,
        nome: str = "moderador",
        senha: str = "123",
        dataEntrada: Optional[date] = None,
        id: Optional[int] = None,
        percursoAtivo: Optional[Registro] = None,
        amigos: Optional[list[Usuario]] = None,
        pedidosAmizade: Optional[list[Usuario]] = None,
        trilhasConcluidas: Optional[list[Registro]] = None,
        trilhasCriadas: Optional[list[Trilha]] = None,
        conquistas: Optional[list[Conquista]] = None,
    ):
        super().__init__(
            nome=nome,
            senha=senha,
            dataEntrada=dataEntrada,
            id=id,
            percursoAtivo=percursoAtivo,
            amigos=amigos,
            pedidosAmizade=pedidosAmizade,
            trilhasConcluidas=trilhasConcluidas,
            trilhasCriadas=trilhasCriadas,
            conquistas=conquistas,
        )

    def aprovarTrilha(self, trilha: Trilha) -> tuple[bool, str]:
        if trilha.aprovadaPor is not None:
            return False, f"A trilha '{trilha.nome}' já foi aprovada por {trilha.aprovadaPor.nome}."
        trilha.aprovadaPor = self
        return True, f"Trilha '{trilha.nome}' aprovada com sucesso."
