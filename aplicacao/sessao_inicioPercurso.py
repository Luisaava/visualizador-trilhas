from __future__ import annotations
from datetime import time
from typing import Optional
from dominio.trilhas import Registro, RegistroGrupo, RegistroIndividual, Trilha
from dominio.usuarios import Usuario
from servicos_tecnicos.mapeador import Mapeador


class SessaoIniciarPercursoIndividual:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def criarRegistro(
        self, t: Trilha, h: time, u: Optional[Usuario] = None
    ) -> RegistroIndividual:
        if u is None:
            raise Exception("Usuário não informado para criação do registro individual.")
        return RegistroIndividual(
            trilha=t,
            usuario=u,
            tempo=None,
            avaliacao=None,
            dificuldade=None,
        )

    def iniciarPercurso(self, t: Trilha, h: time, u: Usuario) -> Registro:
        if u is None:
            raise Exception("Usuário não autenticado.")
        if t is None or t.aprovadaPor is None:
            raise Exception("A trilha selecionada não existe ou ainda não foi aprovada.")
        if u.percursoAtivo is not None:
            raise Exception(
                f"Você já possui um percurso ativo na trilha '{u.percursoAtivo.trilha.nome}'."
            )

        registro = self.criarRegistro(t, h, u)
        registro_salvo = self.__mapeador.salvarRegistro(registro)
        u.percursoAtivo = registro_salvo
        self.__mapeador.atualizarUsuario(u)
        return registro_salvo


class SessaoIniciarPercursoGrupo:
    def __init__(self, mapeador: Optional[Mapeador] = None):
        self.__mapeador: Mapeador = (
            mapeador if mapeador is not None else Mapeador.getInstancia()
        )

    def validarGrupo(self, usuarios: list[Usuario]) -> bool:
        if not usuarios or len(usuarios) < 2:
            raise Exception("Um percurso em grupo exige pelo menos 2 participantes.")

        for i, participante in enumerate(usuarios):
            if any(participante == outro for outro in usuarios[i + 1 :]):
                raise Exception(
                    f"O usuário '{participante.nome}' está duplicado na lista do grupo."
                )

        lider = usuarios[0]
        for participante in usuarios:
            if participante.percursoAtivo is not None:
                raise Exception(
                    f"O usuário '{participante.nome}' já possui um percurso ativo."
                )
            if participante != lider and not any(
                amigo == participante for amigo in lider.amigos
            ):
                raise Exception(
                    f"O usuário '{participante.nome}' não faz parte da sua lista de amigos."
                )
        return True

    def criarRegistroGrupo(
        self, t: Trilha, h: time, usuarios: list[Usuario]
    ) -> RegistroGrupo:
        return RegistroGrupo(
            trilha=t,
            usuarios=usuarios,
            tempo=None,
            avaliacao=None,
            dificuldade=None,
        )

    def iniciarPercursoGrupo(
        self, t: Trilha, h: time, usuarios: list[Usuario]
    ) -> RegistroGrupo:
        if t is None or t.aprovadaPor is None:
            raise Exception("A trilha selecionada não existe ou ainda não foi aprovada.")

        self.validarGrupo(usuarios)
        registro = self.criarRegistroGrupo(t, h, usuarios)
        registro_salvo = self.__mapeador.salvarRegistro(registro)

        for participante in usuarios:
            participante.percursoAtivo = registro_salvo
            self.__mapeador.atualizarUsuario(participante)

        return registro_salvo