from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import psycopg
from dominio.conquistas import Conquista

if TYPE_CHECKING:
    from servicos_tecnicos.mapeador import Mapeador


class MapeadorConquista:
    def __init__(self, conexao: psycopg.Connection, mapeador: Mapeador):
        self.__conexao: psycopg.Connection = conexao
        self.__mapeador: Mapeador = mapeador

    def get(self, id_conquista: int) -> Optional[Conquista]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                "SELECT ID, NOME, DESCRICAO FROM CONQUISTAS WHERE ID = %s;",
                (id_conquista,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha)

    def getPorNome(self, nome: str) -> Optional[Conquista]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                "SELECT ID, NOME, DESCRICAO FROM CONQUISTAS WHERE NOME = %s;",
                (nome,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha)

    def getAll(self) -> list[Conquista]:
        with self.__conexao.cursor() as cur:
            cur.execute("SELECT ID, NOME, DESCRICAO FROM CONQUISTAS ORDER BY ID;")
            linhas = cur.fetchall()
            return [self.__mapearLinha(linha) for linha in linhas]

    def getPorUsuario(self, id_usuario: int) -> list[Conquista]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT c.ID, c.NOME, c.DESCRICAO
                FROM CONQUISTAS c
                INNER JOIN CONQUISTAS_USUARIO cu ON cu.CONQUISTA_ID = c.ID
                WHERE cu.USUARIO_ID = %s
                ORDER BY c.ID;
                """,
                (id_usuario,),
            )
            linhas = cur.fetchall()
            return [self.__mapearLinha(linha) for linha in linhas]

    def put(self, conquista: Conquista) -> Conquista:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                INSERT INTO CONQUISTAS (NOME, DESCRICAO)
                VALUES (%s, %s)
                RETURNING ID;
                """,
                (conquista.nome, conquista.descricao),
            )
            novo_id = cur.fetchone()[0]
            conquista.id = novo_id
        self.__conexao.commit()
        return conquista

    def update(self, conquista: Conquista) -> None:
        if conquista.id is None:
            raise ValueError("Conquista sem ID não pode ser atualizada.")
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                UPDATE CONQUISTAS
                SET NOME = %s, DESCRICAO = %s
                WHERE ID = %s;
                """,
                (conquista.nome, conquista.descricao, conquista.id),
            )
        self.__conexao.commit()

    def remove(self, id_conquista: int) -> bool:
        with self.__conexao.cursor() as cur:
            cur.execute("DELETE FROM CONQUISTAS WHERE ID = %s;", (id_conquista,))
            removido = cur.rowcount > 0
        self.__conexao.commit()
        return removido

    def vincularUsuario(self, id_conquista: int, id_usuario: int) -> None:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                INSERT INTO CONQUISTAS_USUARIO (CONQUISTA_ID, USUARIO_ID)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (id_conquista, id_usuario),
            )
        self.__conexao.commit()

    def __calcularPorcentagemDesbloqueio(self, id_conquista: int) -> float:
        with self.__conexao.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM USUARIOS WHERE TIPO = 'U';")
            total_usuarios = cur.fetchone()[0]
            if total_usuarios == 0:
                return 0.0
            cur.execute(
                "SELECT COUNT(*) FROM CONQUISTAS_USUARIO WHERE CONQUISTA_ID = %s;",
                (id_conquista,),
            )
            total_desbloqueios = cur.fetchone()[0]
            return (total_desbloqueios / total_usuarios) * 100.0

    def __mapearLinha(self, linha: tuple) -> Conquista:
        id_conquista, nome, descricao = linha
        porcentagem = self.__calcularPorcentagemDesbloqueio(id_conquista)
        return Conquista(
            id=id_conquista,
            nome=nome,
            descricao=descricao,
            porcentagemDesbloqueio=porcentagem,
        )
