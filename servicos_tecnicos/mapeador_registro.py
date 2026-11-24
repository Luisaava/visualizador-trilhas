from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import psycopg
from dominio.trilhas import Registro, RegistroIndividual, RegistroGrupo

if TYPE_CHECKING:
    from servicos_tecnicos.mapeador import Mapeador


class MapeadorRegistro:
    def __init__(self, conexao: psycopg.Connection, mapeador: Mapeador):
        self.__conexao: psycopg.Connection = conexao
        self.__mapeador: Mapeador = mapeador

    def get(self, id_registro: int) -> Optional[Registro]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, TRILHA_ID, TEMPO, AVALIACAO, DIFICULDADE, TIPO
                FROM REGISTROS
                WHERE ID = %s;
                """,
                (id_registro,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha)

    def getAll(self) -> list[Registro]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, TRILHA_ID, TEMPO, AVALIACAO, DIFICULDADE, TIPO
                FROM REGISTROS
                ORDER BY ID;
                """
            )
            return [self.__mapearLinha(linha) for linha in cur.fetchall()]

    def getConcluidosPorUsuario(self, id_usuario: int) -> list[Registro]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT r.ID, r.TRILHA_ID, r.TEMPO, r.AVALIACAO, r.DIFICULDADE, r.TIPO
                FROM REGISTROS r
                LEFT JOIN REGISTROS_INDIVIDUAL ri ON ri.REGISTRO_ID = r.ID
                LEFT JOIN REGISTROS_GRUPO rg ON rg.REGISTRO_ID = r.ID
                WHERE (ri.USUARIO_ID = %s OR rg.USUARIO_ID = %s)
                  AND r.TEMPO IS NOT NULL
                GROUP BY r.ID, r.TRILHA_ID, r.TEMPO, r.AVALIACAO, r.DIFICULDADE, r.TIPO
                ORDER BY r.ID;
                """,
                (id_usuario, id_usuario),
            )
            return [self.__mapearLinha(linha) for linha in cur.fetchall()]

    def put(self, registro: Registro) -> Registro:
        if registro.trilha.id is None:
            raise ValueError("A trilha do registro precisa estar persistida antes de criar o registro.")

        tipo = "G" if isinstance(registro, RegistroGrupo) else "I"
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                INSERT INTO REGISTROS (TRILHA_ID, TEMPO, AVALIACAO, DIFICULDADE, TIPO)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING ID;
                """,
                (
                    registro.trilha.id,
                    registro.tempo,
                    registro.avaliacao,
                    registro.dificuldade,
                    tipo,
                ),
            )
            registro.id = cur.fetchone()[0]

            if isinstance(registro, RegistroIndividual):
                if registro.usuario.id is None:
                    raise ValueError("Usuário do registro individual sem ID.")
                cur.execute(
                    """
                    INSERT INTO REGISTROS_INDIVIDUAL (REGISTRO_ID, USUARIO_ID)
                    VALUES (%s, %s);
                    """,
                    (registro.id, registro.usuario.id),
                )
            elif isinstance(registro, RegistroGrupo):
                for membro in registro.usuarios:
                    if membro.id is None:
                        raise ValueError("Membro do registro em grupo sem ID.")
                    cur.execute(
                        """
                        INSERT INTO REGISTROS_GRUPO (REGISTRO_ID, USUARIO_ID)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                        """,
                        (registro.id, membro.id),
                    )
        self.__conexao.commit()
        return registro

    def update(self, registro: Registro) -> None:
        if registro.id is None:
            raise ValueError("Registro sem ID não pode ser atualizado.")
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                UPDATE REGISTROS
                SET TRILHA_ID = %s,
                    TEMPO = %s,
                    AVALIACAO = %s,
                    DIFICULDADE = %s
                WHERE ID = %s;
                """,
                (
                    registro.trilha.id,
                    registro.tempo,
                    registro.avaliacao,
                    registro.dificuldade,
                    registro.id,
                ),
            )
        self.__conexao.commit()

    def remove(self, id_registro: int) -> bool:
        with self.__conexao.cursor() as cur:
            cur.execute("DELETE FROM REGISTROS WHERE ID = %s;", (id_registro,))
            removido = cur.rowcount > 0
        self.__conexao.commit()
        return removido

    def __mapearLinha(self, linha: tuple) -> Registro:
        id_registro, trilha_id, tempo, avaliacao, dificuldade, tipo = linha
        trilha = self.__mapeador.getTrilha(trilha_id)
        if trilha is None:
            raise ValueError(f"Trilha ID {trilha_id} não encontrada para o Registro ID {id_registro}.")

        aval_float = float(avaliacao) if avaliacao is not None else None
        dif_int = int(dificuldade) if dificuldade is not None else None

        if tipo == "G":
            with self.__conexao.cursor() as cur:
                cur.execute(
                    """
                    SELECT USUARIO_ID
                    FROM REGISTROS_GRUPO
                    WHERE REGISTRO_ID = %s
                    ORDER BY USUARIO_ID;
                    """,
                    (id_registro,),
                )
                membros_ids = [row[0] for row in cur.fetchall()]
            membros = []
            for uid in membros_ids:
                u = self.__mapeador.getUsuarioBasico(uid)
                if u is not None:
                    membros.append(u)
            return RegistroGrupo(
                id=id_registro,
                trilha=trilha,
                usuarios=membros,
                tempo=tempo,
                avaliacao=aval_float,
                dificuldade=dif_int,
            )
        else:
            with self.__conexao.cursor() as cur:
                cur.execute(
                    "SELECT USUARIO_ID FROM REGISTROS_INDIVIDUAL WHERE REGISTRO_ID = %s;",
                    (id_registro,),
                )
                row = cur.fetchone()
            usuario = self.__mapeador.getUsuarioBasico(row[0]) if row else None
            if usuario is None:
                raise ValueError(f"Usuário não encontrado para RegistroIndividual ID {id_registro}.")
            return RegistroIndividual(
                id=id_registro,
                trilha=trilha,
                usuario=usuario,
                tempo=tempo,
                avaliacao=aval_float,
                dificuldade=dif_int,
            )
