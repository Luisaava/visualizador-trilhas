from __future__ import annotations
from datetime import time
from typing import Optional, TYPE_CHECKING
import psycopg
from dominio.trilhas import Trilha
from dominio.usuarios import Usuario, Moderador

if TYPE_CHECKING:
    from servicos_tecnicos.mapeador import Mapeador


class MapeadorTrilha:
    def __init__(self, conexao: psycopg.Connection, mapeador: Mapeador):
        self.__conexao: psycopg.Connection = conexao
        self.__mapeador: Mapeador = mapeador

    def get(self, id_trilha: int) -> Optional[Trilha]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                       DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
                FROM TRILHAS
                WHERE ID = %s;
                """,
                (id_trilha,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha)

    def getPorNome(self, nome: str) -> Optional[Trilha]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                       DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
                FROM TRILHAS
                WHERE LOWER(NOME) = LOWER(%s);
                """,
                (nome,),
            )
            linha = cur.fetchone()
            if linha is None:
                return None
            return self.__mapearLinha(linha)

    def getAll(self) -> list[Trilha]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                       DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
                FROM TRILHAS
                ORDER BY ID;
                """
            )
            return [self.__mapearLinha(linha) for linha in cur.fetchall()]

    def getAprovadas(self) -> list[Trilha]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                       DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
                FROM TRILHAS
                WHERE APROVADOR_ID IS NOT NULL
                ORDER BY NOME;
                """
            )
            return [self.__mapearLinha(linha) for linha in cur.fetchall()]

    def getPendentes(self) -> list[Trilha]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                       DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
                FROM TRILHAS
                WHERE APROVADOR_ID IS NULL
                ORDER BY ID;
                """
            )
            return [self.__mapearLinha(linha) for linha in cur.fetchall()]

    def getCriadasPorUsuario(self, id_usuario: int) -> list[Trilha]:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                       DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
                FROM TRILHAS
                WHERE CRIADOR_ID = %s
                ORDER BY ID;
                """,
                (id_usuario,),
            )
            return [self.__mapearLinha(linha) for linha in cur.fetchall()]

    def buscarComFiltros(
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
        condicoes = ["APROVADOR_ID IS NOT NULL"]
        parametros: list = []

        if nome:
            condicoes.append("NOME ILIKE %s")
            parametros.append(f"%{nome}%")
        if local_inicio:
            condicoes.append("LOCAL_INICIO ILIKE %s")
            parametros.append(f"%{local_inicio}%")
        if local_fim:
            condicoes.append("LOCAL_FIM ILIKE %s")
            parametros.append(f"%{local_fim}%")
        if dificuldade_min is not None:
            condicoes.append("DIFICULDADE >= %s")
            parametros.append(dificuldade_min)
        if dificuldade_max is not None:
            condicoes.append("DIFICULDADE <= %s")
            parametros.append(dificuldade_max)
        if comprimento_min is not None:
            condicoes.append("COMPRIMENTO >= %s")
            parametros.append(comprimento_min)
        if comprimento_max is not None:
            condicoes.append("COMPRIMENTO <= %s")
            parametros.append(comprimento_max)
        if avaliacao_min is not None:
            condicoes.append("AVALIACAO >= %s")
            parametros.append(avaliacao_min)
        if duracao_max is not None:
            condicoes.append("DURACAO_MEDIA <= %s")
            parametros.append(duracao_max)

        where_clause = " AND ".join(condicoes)
        query = f"""
            SELECT ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                   DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
            FROM TRILHAS
            WHERE {where_clause}
            ORDER BY NOME;
        """
        with self.__conexao.cursor() as cur:
            cur.execute(query, tuple(parametros))
            return [self.__mapearLinha(linha) for linha in cur.fetchall()]

    def put(self, trilha: Trilha) -> Trilha:
        criador_id = trilha.criador.id if trilha.criador else None
        aprovador_id = trilha.aprovadaPor.id if trilha.aprovadaPor else None
        try:
            with self.__conexao.cursor() as cur:
                cur.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM TRILHAS;")
                proximo_id = int(cur.fetchone()[0])

                cur.execute(
                    """
                    INSERT INTO TRILHAS (
                        ID, NOME, LOCAL_INICIO, LOCAL_FIM, COMPRIMENTO, AVALIACAO,
                        DIFICULDADE, VARIACAO_ALTITUDE, DURACAO_MEDIA, CRIADOR_ID, APROVADOR_ID
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING ID;
                    """,
                    (
                        proximo_id,
                        trilha.nome,
                        trilha.localInicio,
                        trilha.localFim,
                        trilha.comprimento,
                        trilha.avaliacao,
                        trilha.dificuldade,
                        trilha.variacaoAltitude,
                        trilha.duracaoMedia,
                        criador_id,
                        aprovador_id,
                    ),
                )
                trilha.id = cur.fetchone()[0]
            self.__conexao.commit()
            return trilha
        except Exception:
            self.__conexao.rollback()
            raise

    def update(self, trilha: Trilha) -> None:
        if trilha.id is None:
            raise ValueError("Trilha sem ID não pode ser atualizada.")
        criador_id = trilha.criador.id if trilha.criador else None
        aprovador_id = trilha.aprovadaPor.id if trilha.aprovadaPor else None
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                UPDATE TRILHAS
                SET NOME = %s,
                    LOCAL_INICIO = %s,
                    LOCAL_FIM = %s,
                    COMPRIMENTO = %s,
                    AVALIACAO = %s,
                    DIFICULDADE = %s,
                    VARIACAO_ALTITUDE = %s,
                    DURACAO_MEDIA = %s,
                    CRIADOR_ID = %s,
                    APROVADOR_ID = %s
                WHERE ID = %s;
                """,
                (
                    trilha.nome,
                    trilha.localInicio,
                    trilha.localFim,
                    trilha.comprimento,
                    trilha.avaliacao,
                    trilha.dificuldade,
                    trilha.variacaoAltitude,
                    trilha.duracaoMedia,
                    criador_id,
                    aprovador_id,
                    trilha.id,
                ),
            )
        self.__conexao.commit()

    def recalcularAvaliacao(self, id_trilha: int) -> float:
        with self.__conexao.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(AVG(AVALIACAO), 0.0)
                FROM REGISTROS
                WHERE TRILHA_ID = %s AND AVALIACAO IS NOT NULL;
                """,
                (id_trilha,),
            )
            media = float(cur.fetchone()[0])
            cur.execute(
                "UPDATE TRILHAS SET AVALIACAO = %s WHERE ID = %s;",
                (round(media, 2), id_trilha),
            )
        self.__conexao.commit()
        return round(media, 2)

    def remove(self, id_trilha: int) -> bool:
        with self.__conexao.cursor() as cur:
            cur.execute("DELETE FROM TRILHAS WHERE ID = %s;", (id_trilha,))
            removida = cur.rowcount > 0
        self.__conexao.commit()
        return removida

    def __mapearLinha(self, linha: tuple) -> Trilha:
        (
            id_trilha,
            nome,
            local_inicio,
            local_fim,
            comprimento,
            avaliacao,
            dificuldade,
            variacao_altitude,
            duracao_media,
            criador_id,
            aprovador_id,
        ) = linha

        criador: Usuario
        if criador_id is not None:
            criador_encontrado = self.__mapeador.getUsuarioBasico(criador_id)
            criador = criador_encontrado if criador_encontrado else Usuario(nome="Usuário removido", senha="", id=criador_id)
        else:
            criador = Usuario(nome="Sistema", senha="")

        aprovador: Optional[Moderador] = None
        if aprovador_id is not None:
            aprovador_encontrado = self.__mapeador.getUsuarioBasico(aprovador_id)
            if isinstance(aprovador_encontrado, Moderador):
                aprovador = aprovador_encontrado
            elif aprovador_encontrado is not None:
                aprovador = Moderador(
                    nome=aprovador_encontrado.nome,
                    senha=aprovador_encontrado.senha,
                    dataEntrada=aprovador_encontrado.dataEntrada,
                    id=aprovador_encontrado.id,
                )

        return Trilha(
            id=id_trilha,
            nome=nome,
            localInicio=local_inicio,
            localFim=local_fim,
            comprimento=float(comprimento),
            avaliacao=float(avaliacao),
            dificuldade=int(dificuldade),
            variacaoAltitude=int(variacao_altitude),
            duracaoMedia=duracao_media,
            criador=criador,
            aprovadaPor=aprovador,
        )
