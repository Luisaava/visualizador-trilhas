from __future__ import annotations
from typing import Optional
from dominio.usuarios import Usuario
from servicos_tecnicos.mapeador import Mapeador


class SessaoAmizade:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def buscarUsuarioPorNome(self, nome: str) -> Usuario:
        if not nome or not nome.strip():
            raise Exception("Informe o nome do usuário.")
        usuario = self.__mapeador.getUsuarioPorNome(nome.strip())
        if usuario is None:
            raise Exception(f"Usuário '{nome.strip()}' não encontrado.")
        return usuario

    def adicionarAmigo(self, remetente: Usuario, destinatario: Usuario) -> None:
        if destinatario is None:
            raise Exception("Usuário destinatário não encontrado.")

        sucesso, msg = remetente.adicionarAmigo(destinatario)
        if not sucesso:
            raise Exception(msg)

        self.__mapeador.registrarPedidoAmizade(remetente, destinatario)

    def aceitarPedido(self, usuario: Usuario, remetente: Usuario) -> None:
        if remetente is None:
            raise Exception("Usuário remetente não encontrado.")

        sucesso, msg = usuario.aceitarPedido(remetente)
        if not sucesso:
            raise Exception(msg)

        self.__mapeador.aceitarPedidoAmizade(remetente, usuario)

    def recusarPedido(self, usuario: Usuario, nome_remetente: str) -> None:
        if not nome_remetente or not nome_remetente.strip():
            raise Exception("Informe o nome do remetente.")

        nome_limpo = nome_remetente.strip()
        remetente = next(
            (p for p in usuario.pedidosAmizade if p.nome == nome_limpo),
            None,
        )
        if remetente is None:
            remetente = self.buscarUsuarioPorNome(nome_limpo)

        sucesso, msg = usuario.recusarPedido(remetente)
        if not sucesso:
            raise Exception(msg)

        self.__mapeador.recusarPedidoAmizade(remetente, usuario)

    def recarregarUsuario(self, usuario: Usuario) -> Usuario:
        if usuario.id is not None:
            atualizado = self.__mapeador.getUsuario(usuario.id)
            if atualizado is not None:
                return atualizado
        return usuario