from __future__ import annotations
import os
from datetime import time
from pathlib import Path
from typing import Optional
import psycopg

from dominio.usuarios import Usuario, Moderador
from dominio.trilhas import Trilha, Registro
from dominio.conquistas import Conquista
from servicos_tecnicos.mapeador_usuario import MapeadorUsuario
from servicos_tecnicos.mapeador_trilha import MapeadorTrilha
from servicos_tecnicos.mapeador_registro import MapeadorRegistro
from servicos_tecnicos.mapeador_conquista import MapeadorConquista


class Mapeador:
    """Fachada Singleton que centraliza o acesso aos mapeadores PostgreSQL via psycopg."""

    __instancia: Optional[Mapeador] = None

    def __init__(self, dsn: Optional[str] = None):
        if Mapeador.__instancia is not None:
            raise RuntimeError("Use Mapeador.getInstancia() para obter a instância Singleton.")

        if dsn is None:
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            #dbname = os.getenv("DB_NAME", "visualizador_trilhas")
            user = os.getenv("DB_USER", "postgres")
            password = os.getenv("DB_PASSWORD", "postgres")
            dsn = f"host={host} port={port} user={user} password={password}"

        self.__conexao: psycopg.Connection = psycopg.connect(dsn)
        self.__mapeadorUsuario: MapeadorUsuario = MapeadorUsuario(self.__conexao, self)
        self.__mapeadorTrilha: MapeadorTrilha = MapeadorTrilha(self.__conexao, self)
        self.__mapeadorRegistro: MapeadorRegistro = MapeadorRegistro(self.__conexao, self)
        self.__mapeadorConquista: MapeadorConquista = MapeadorConquista(self.__conexao, self)

    @classmethod
    def getInstancia(cls, dsn: Optional[str] = None) -> Mapeador:
        if cls.__instancia is None:
            cls.__instancia = cls(dsn=dsn)
        return cls.__instancia

    def inicializarBanco(self) -> None:
        schema_path = Path(__file__).parent / "schema.sql"
        sql = schema_path.read_text(encoding="utf-8")
        with self.__conexao.cursor() as cur:
            cur.execute(sql)
        self.__conexao.commit()

    def fecharConexao(self) -> None:
        if self.__conexao and not self.__conexao.closed:
            self.__conexao.close()
        Mapeador.__instancia = None

    # --- Operações de Usuário ---
    def getUsuario(self, id_usuario: int) -> Optional[Usuario]:
        return self.__mapeadorUsuario.get(id_usuario)

    def getUsuarioBasico(self, id_usuario: int) -> Optional[Usuario]:
        return self.__mapeadorUsuario.getBasico(id_usuario)

    def getUsuarioPorNome(self, nome: str) -> Optional[Usuario]:
        return self.__mapeadorUsuario.getPorNome(nome)

    def getTodosUsuarios(self) -> list[Usuario]:
        return self.__mapeadorUsuario.getAll()

    def salvarUsuario(self, usuario: Usuario) -> Usuario:
        return self.__mapeadorUsuario.put(usuario)

    def atualizarUsuario(self, usuario: Usuario) -> None:
        self.__mapeadorUsuario.update(usuario)

    def removerUsuario(self, id_usuario: int) -> bool:
        return self.__mapeadorUsuario.remove(id_usuario)

    def registrarPedidoAmizade(self, remetente: Usuario, destinatario: Usuario) -> None:
        if remetente.id is not None and destinatario.id is not None:
            self.__mapeadorUsuario.adicionarPedidoAmizade(remetente.id, destinatario.id)

    def aceitarPedidoAmizade(self, remetente: Usuario, destinatario: Usuario) -> None:
        if remetente.id is not None and destinatario.id is not None:
            self.__mapeadorUsuario.removerPedidoAmizade(remetente.id, destinatario.id)
            self.__mapeadorUsuario.adicionarAmizade(remetente.id, destinatario.id)

    def recusarPedidoAmizade(self, remetente: Usuario, destinatario: Usuario) -> None:
        if remetente.id is not None and destinatario.id is not None:
            self.__mapeadorUsuario.removerPedidoAmizade(remetente.id, destinatario.id)

    # --- Operações de Trilha ---
    def getTrilha(self, id_trilha: int) -> Optional[Trilha]:
        return self.__mapeadorTrilha.get(id_trilha)

    def getTrilhaPorNome(self, nome: str) -> Optional[Trilha]:
        return self.__mapeadorTrilha.getPorNome(nome)

    def getTodasTrilhas(self) -> list[Trilha]:
        return self.__mapeadorTrilha.getAll()

    def getTrilhasAprovadas(self) -> list[Trilha]:
        return self.__mapeadorTrilha.getAprovadas()

    def getTrilhasPendentes(self) -> list[Trilha]:
        return self.__mapeadorTrilha.getPendentes()

    def getTrilhasCriadasUsuario(self, id_usuario: int) -> list[Trilha]:
        return self.__mapeadorTrilha.getCriadasPorUsuario(id_usuario)

    def buscarTrilhasComFiltros(
        self,
        nome: Optional[str] = None,
        local_inicio: Optional[str] = None,
        local_fim: Optional[str] = None,
        dificuldade_min: Optional[int] = None,
        dificuldade_max: Optional[int] = None,
        comprimento_min: Optional[float] = None,
        comprimento_max: Optional[float] = None,
        avaliacao_min: Optional[float] = None,
        duracao_max: Optional[time] = None,
    ) -> list[Trilha]:
        return self.__mapeadorTrilha.buscarComFiltros(
            nome=nome,
            local_inicio=local_inicio,
            local_fim=local_fim,
            dificuldade_min=dificuldade_min,
            dificuldade_max=dificuldade_max,
            comprimento_min=comprimento_min,
            comprimento_max=comprimento_max,
            avaliacao_min=avaliacao_min,
            duracao_max=duracao_max,
        )

    def salvarTrilha(self, trilha: Trilha) -> Trilha:
        return self.__mapeadorTrilha.put(trilha)

    def atualizarTrilha(self, trilha: Trilha) -> None:
        self.__mapeadorTrilha.update(trilha)

    def recalcularAvaliacaoTrilha(self, id_trilha: int) -> float:
        return self.__mapeadorTrilha.recalcularAvaliacao(id_trilha)

    def removerTrilha(self, id_trilha: int) -> bool:
        return self.__mapeadorTrilha.remove(id_trilha)

    # --- Operações de Registro ---
    def getRegistro(self, id_registro: int) -> Optional[Registro]:
        return self.__mapeadorRegistro.get(id_registro)

    def getTodosRegistros(self) -> list[Registro]:
        return self.__mapeadorRegistro.getAll()

    def getRegistrosConcluidosUsuario(self, id_usuario: int) -> list[Registro]:
        return self.__mapeadorRegistro.getConcluidosPorUsuario(id_usuario)

    def salvarRegistro(self, registro: Registro) -> Registro:
        return self.__mapeadorRegistro.put(registro)

    def atualizarRegistro(self, registro: Registro) -> None:
        self.__mapeadorRegistro.update(registro)

    def removerRegistro(self, id_registro: int) -> bool:
        return self.__mapeadorRegistro.remove(id_registro)

    # --- Operações de Conquista ---
    def getConquista(self, id_conquista: int) -> Optional[Conquista]:
        return self.__mapeadorConquista.get(id_conquista)

    def getConquistaPorNome(self, nome: str) -> Optional[Conquista]:
        return self.__mapeadorConquista.getPorNome(nome)

    def getTodasConquistas(self) -> list[Conquista]:
        return self.__mapeadorConquista.getAll()

    def getConquistasUsuario(self, id_usuario: int) -> list[Conquista]:
        return self.__mapeadorConquista.getPorUsuario(id_usuario)

    def salvarConquista(self, conquista: Conquista) -> Conquista:
        return self.__mapeadorConquista.put(conquista)

    def vincularConquistaUsuario(self, id_conquista: int, id_usuario: int) -> None:
        self.__mapeadorConquista.vincularUsuario(id_conquista, id_usuario)
