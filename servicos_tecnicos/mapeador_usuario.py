from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import psycopg
from dominio.usuarios import Usuario, Moderador

if TYPE_CHECKING:
    from servicos_tecnicos.mapeador import Mapeador


class MapeadorUsuario:
    def __init__(self, conexao: psycopg.Connection, mapeador: Mapeador):
        self.__conexao: psycopg.Connection = conexao
        self.__mapeador: Mapeador = mapeador

    def get(self, id_usuario: int) -> Optional[Usuario]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, SENHA, ENTRADA, PERCURSO_ATIVO, TIPO
                FROM USUARIOS
                WHERE ID = %s;
                """,
                (id_usuario,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha, carregar_relacoes=True)

    def getBasico(self, id_usuario: int) -> Optional[Usuario]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, SENHA, ENTRADA, PERCURSO_ATIVO, TIPO
                FROM USUARIOS
                WHERE ID = %s;
                """,
                (id_usuario,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha, carregar_relacoes=False)

    def getPorNome(self, nome: str) -> Optional[Usuario]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, SENHA, ENTRADA, PERCURSO_ATIVO, TIPO
                FROM USUARIOS
                WHERE NOME = %s;
                """,
                (nome,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha, carregar_relacoes=True)

    def getAll(self) -> list[Usuario]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, SENHA, ENTRADA, PERCURSO_ATIVO, TIPO
                FROM USUARIOS
                ORDER BY ID;
                """
            )
            return [self.__mapearLinha(linha, carregar_relacoes=False) for linha in cur.fetchall()]

    def put(self, usuario: Usuario) -> Usuario:
        tipo = "M" if isinstance(usuario, Moderador) else "U"
        percurso_id = usuario.percursoAtivo.id if usuario.percursoAtivo else None
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                INSERT INTO USUARIOS (NOME, SENHA, ENTRADA, PERCURSO_ATIVO, TIPO)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING ID;
                """,
                (usuario.nome, usuario.senha, usuario.dataEntrada, percurso_id, tipo),
            )
            usuario.id = cur.fetchone()[0]
        self.__conexao.commit()
        return usuario

    def update(self, usuario: Usuario) -> None:
        if usuario.id is None:
            raise ValueError("Usuário sem ID não pode ser atualizado.")
        tipo = "M" if isinstance(usuario, Moderador) else "U"
        percurso_id = usuario.percursoAtivo.id if usuario.percursoAtivo else None
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                UPDATE USUARIOS
                SET NOME = %s,
                    SENHA = %s,
                    ENTRADA = %s,
                    PERCURSO_ATIVO = %s,
                    TIPO = %s
                WHERE ID = %s;
                """,
                (
                    usuario.nome,
                    usuario.senha,
                    usuario.dataEntrada,
                    percurso_id,
                    tipo,
                    usuario.id,
                ),
            )
        self.__conexao.commit()

    def adicionarPedidoAmizade(self, id_remetente: int, id_destinatario: int) -> None:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                INSERT INTO PEDIDOS_AMIZADE (USUARIO1_ID, USUARIO2_ID)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (id_remetente, id_destinatario),
            )
        self.__conexao.commit()

    def removerPedidoAmizade(self, id_remetente: int, id_destinatario: int) -> None:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                DELETE FROM PEDIDOS_AMIZADE
                WHERE USUARIO1_ID = %s AND USUARIO2_ID = %s;
                """,
                (id_remetente, id_destinatario),
            )
        self.__conexao.commit()

    def adicionarAmizade(self, id_usuario1: int, id_usuario2: int) -> None:
        u1, u2 = sorted([id_usuario1, id_usuario2])
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                INSERT INTO AMIGOS (USUARIO1_ID, USUARIO2_ID)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (u1, u2),
            )
        self.__conexao.commit()

    def remove(self, id_usuario: int) -> bool:
        with self.__conexao.cursor() as cur:
            # Limpa registros individuais exclusivos do usuário
            cur.execute(
                """
                DELETE FROM REGISTROS
                WHERE ID IN (
                    SELECT REGISTRO_ID FROM REGISTROS_INDIVIDUAL WHERE USUARIO_ID = %s
                );
                """,
                (id_usuario,),
            )
            # Remove participação em grupos
            cur.execute(
                "DELETE FROM REGISTROS_GRUPO WHERE USUARIO_ID = %s;",
                (id_usuario,),
            )
            # Remove registros de grupo que ficaram vazios
            cur.execute(
                """
                DELETE FROM REGISTROS
                WHERE TIPO = 'G'
                  AND ID NOT IN (SELECT DISTINCT REGISTRO_ID FROM REGISTROS_GRUPO);
                """
            )
            cur.execute("DELETE FROM USUARIOS WHERE ID = %s;", (id_usuario,))
            removido = cur.rowcount > 0
        self.__conexao.commit()
        return removido

    def __mapearLinha(self, linha: tuple, carregar_relacoes: bool = True) -> Usuario:
        id_usuario, nome, senha, entrada, percurso_ativo_id, tipo = linha
        classe = Moderador if tipo == "M" else Usuario
        usuario = classe(
            id=id_usuario,
            nome=nome,
            senha=senha,
            dataEntrada=entrada,
        )

        if not carregar_relacoes:
            return usuario

        if percurso_ativo_id is not None:
            usuario.percursoAtivo = self.__mapeador.getRegistro(percurso_ativo_id)

        with self.__conexao.cursor() as cur:
            # Amigos (bidirecional)
            cur.execute(
                """
                SELECT CASE WHEN USUARIO1_ID = %s THEN USUARIO2_ID ELSE USUARIO1_ID END
                FROM AMIGOS
                WHERE USUARIO1_ID = %s OR USUARIO2_ID = %s;
                """,
                (id_usuario, id_usuario, id_usuario),
            )
            amigos_ids = [r[0] for r in cur.fetchall()]

            # Pedidos de amizade recebidos (USUARIO1_ID enviou para USUARIO2_ID)
            cur.execute(
                """
                SELECT USUARIO1_ID
                FROM PEDIDOS_AMIZADE
                WHERE USUARIO2_ID = %s;
                """,
                (id_usuario,),
            )
            pedidos_ids = [r[0] for r in cur.fetchall()]

        usuario.amigos = [
            amigo for aid in amigos_ids if (amigo := self.getBasico(aid)) is not None
        ]
        usuario.pedidosAmizade = [
            rem for pid in pedidos_ids if (rem := self.getBasico(pid)) is not None
        ]
        usuario.trilhasConcluidas = self.__mapeador.getRegistrosConcluidosUsuario(id_usuario)
        usuario.trilhasCriadas = self.__mapeador.getTrilhasCriadasUsuario(id_usuario)
        usuario.conquistas = self.__mapeador.getConquistasUsuario(id_usuario)

        return usuario
