from __future__ import annotations
from datetime import time
from servicos_tecnicos.mapeador import Mapeador
from dominio.usuarios import Usuario, Moderador
from dominio.trilhas import Trilha
from dominio.conquistas import Conquista
from aplicacao.sessao_cadastroUsuario import SessaoCadastroUsuario
from aplicacao.sessao_login import SessaoLogin
from apresentacao.interface_inicial import InterfaceInicial


def carregar_dados_iniciais(mapeador: Mapeador) -> None:
    """Popula dados iniciais no banco caso ainda não existam."""
    mod = mapeador.getUsuarioPorNome("moderador")
    if mod is None:
        mod = Moderador(nome="moderador", senha="123")
        mapeador.salvarUsuario(mod)

    admin_teste = mapeador.getUsuarioPorNome("AdminTeste")
    if admin_teste is None:
        admin_teste = Usuario(nome="AdminTeste", senha="123")
        mapeador.salvarUsuario(admin_teste)

    conquistas_padrao = [
        ("Primeiros Passos", "Concluiu sua primeira trilha."),
        ("Explorador Dedicado", "Concluiu 5 trilhas no sistema."),
        ("Maratonista das Trilhas", "Percorreu mais de 20 km acumulados em trilhas."),
        ("Espírito de Equipe", "Concluiu uma trilha em grupo com amigos."),
    ]
    for nome_c, desc_c in conquistas_padrao:
        if mapeador.getConquistaPorNome(nome_c) is None:
            mapeador.salvarConquista(Conquista(nome=nome_c, descricao=desc_c))

    if not mapeador.getTodasTrilhas() and isinstance(mod, Moderador):
        t1 = Trilha(
            nome="Trilha da Costa da Lagoa",
            localInicio="Canto dos Araçás",
            localFim="Centrinho da Costa",
            comprimento=7.5,
            dificuldade=4,
            variacaoAltitude=150,
            duracaoMedia=time(2, 30, 0),
            criador=admin_teste,
            avaliacao=0.0,
            aprovadaPor=mod,
        )
        t2 = Trilha(
            nome="Trilha do Gravatá",
            localInicio="Praia Mole",
            localFim="Praia do Gravatá",
            comprimento=1.2,
            dificuldade=3,
            variacaoAltitude=60,
            duracaoMedia=time(0, 45, 0),
            criador=admin_teste,
            avaliacao=0.0,
            aprovadaPor=mod,
        )
        t3 = Trilha(
            nome="Trilha do Morro do Lampião",
            localInicio="Campeche",
            localFim="Mirante do Lampião",
            comprimento=2.8,
            dificuldade=5,
            variacaoAltitude=210,
            duracaoMedia=time(1, 15, 0),
            criador=admin_teste,
            avaliacao=0.0,
            aprovadaPor=None,
        )
        mapeador.salvarTrilha(t1)
        mapeador.salvarTrilha(t2)
        mapeador.salvarTrilha(t3)


def main() -> None:
    mapeador = Mapeador.getInstancia()
    try:
        mapeador.inicializarBanco()
        carregar_dados_iniciais(mapeador)

        sessao_cadastro = SessaoCadastroUsuario(mapeador)
        sessao_login = SessaoLogin(mapeador)

        app = InterfaceInicial(sessao_cadastro, sessao_login)
        app.executar()
    finally:
        mapeador.fecharConexao()


if __name__ == "__main__":
    main()
