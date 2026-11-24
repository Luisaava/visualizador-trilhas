from __future__ import annotations
from datetime import time
from typing import Optional
from dominio.trilhas import RegistroIndividual, RegistroGrupo
from dominio.usuarios import Usuario
from servicos_tecnicos.mapeador import Mapeador


class _GerenciadorConclusao:
    """Auxiliar interno para avaliação de conquistas após conclusão de trilha."""

    @staticmethod
    def verificarConquistas(usuario: Usuario, mapeador: Mapeador) -> list[str]:
        if usuario.id is None:
            return []
        desbloqueadas: list[str] = []
        total_concluidas = len(usuario.trilhasConcluidas)
        distancia_total = sum(r.trilha.comprimento for r in usuario.trilhasConcluidas)
        tem_grupo = any(isinstance(r, RegistroGrupo) for r in usuario.trilhasConcluidas)

        regras = [
            ("Primeiros Passos", total_concluidas >= 1),
            ("Explorador Dedicado", total_concluidas >= 5),
            ("Maratonista das Trilhas", distancia_total >= 20.0),
            ("Espírito de Equipe", tem_grupo),
        ]

        for nome_conquista, atingiu in regras:
            if atingiu:
                conquista = mapeador.getConquistaPorNome(nome_conquista)
                if conquista is not None and conquista.id is not None:
                    if usuario.adicionarConquista(conquista):
                        mapeador.vincularConquistaUsuario(conquista.id, usuario.id)
                        desbloqueadas.append(conquista.nome)
        return desbloqueadas


class SessaoFinalizarPercursoIndividual:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def finalizarPercurso(
        self,
        u: Usuario,
        duracao: time,
        nota: float,
        dificuldade: Optional[int] = None,
    ) -> None:
        if u is None or u.percursoAtivo is None:
            raise Exception("Você não possui um percurso ativo para finalizar.")
        if not isinstance(u.percursoAtivo, RegistroIndividual):
            raise Exception(
                "Seu percurso ativo é em grupo. Utilize a opção de finalizar percurso em grupo."
            )
        if duracao == time(0, 0):
            raise Exception("A duração do percurso deve ser maior que zero.")
        if nota < 0.0 or nota > 5.0:
            raise Exception("A nota da trilha deve estar entre 0.0 e 5.0.")
        if dificuldade is not None and (dificuldade < 1 or dificuldade > 10):
            raise Exception("A dificuldade percebida deve estar entre 1 e 10.")

        registro = u.percursoAtivo
        registro.tempo = duracao
        registro.avaliacao = nota
        registro.dificuldade = (
            dificuldade if dificuldade is not None else registro.trilha.dificuldade
        )
        self.__mapeador.atualizarRegistro(registro)

        u.percursoAtivo = None
        if not any(r.id == registro.id for r in u.trilhasConcluidas):
            u.trilhasConcluidas.append(registro)
        self.__mapeador.atualizarUsuario(u)

        if registro.trilha.id is not None:
            nova_media = self.__mapeador.recalcularAvaliacaoTrilha(registro.trilha.id)
            registro.trilha.avaliacao = nova_media

        _GerenciadorConclusao.verificarConquistas(u, self.__mapeador)


class SessaoFinalizarPercursoGrupo:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def calcularNotaMedia(self, notas: list[float]) -> float:
        if not notas:
            raise Exception("Informe pelo menos uma nota para calcular a média do grupo.")
        for nota in notas:
            if nota < 0.0 or nota > 5.0:
                raise Exception(
                    f"Nota inválida ({nota}). Todas as avaliações devem estar entre 0.0 e 5.0."
                )
        return sum(notas) / len(notas)

    def finalizarPercursoGrupo(
        self,
        u: Usuario,
        duracao: time,
        notas: list[float],
        dificuldade: Optional[int] = None,
    ) -> None:
        if u is None or u.percursoAtivo is None:
            raise Exception("Você não possui um percurso ativo para finalizar.")
        if not isinstance(u.percursoAtivo, RegistroGrupo):
            raise Exception(
                "Seu percurso ativo é individual. Utilize a opção de finalizar percurso individual."
            )
        if duracao == time(0, 0):
            raise Exception("A duração do percurso deve ser maior que zero.")
        if dificuldade is not None and (dificuldade < 1 or dificuldade > 10):
            raise Exception("A dificuldade percebida deve estar entre 1 e 10.")

        registro = u.percursoAtivo
        if len(notas) != registro.qtdUsuarios:
            raise Exception(
                f"Informe exatamente {registro.qtdUsuarios} notas (uma para cada participante do grupo)."
            )

        nota_media = self.calcularNotaMedia(notas)
        registro.tempo = duracao
        registro.avaliacao = nota_media
        registro.dificuldade = (
            dificuldade if dificuldade is not None else registro.trilha.dificuldade
        )
        self.__mapeador.atualizarRegistro(registro)

        for membro in registro.usuarios:
            membro_db = (
                self.__mapeador.getUsuario(membro.id) if membro.id is not None else membro
            )
            alvo = membro_db if membro_db is not None else membro
            alvo.percursoAtivo = None
            if not any(r.id == registro.id for r in alvo.trilhasConcluidas):
                alvo.trilhasConcluidas.append(registro)
            self.__mapeador.atualizarUsuario(alvo)
            _GerenciadorConclusao.verificarConquistas(alvo, self.__mapeador)

        if registro.trilha.id is not None:
            nova_media = self.__mapeador.recalcularAvaliacaoTrilha(registro.trilha.id)
            registro.trilha.avaliacao = nova_media