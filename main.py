from servicos_tecnicos.persistencia import PersistenciaJSON
from aplicacao.sessao_cadastroUsuario import SessaoCadastro
from aplicacao.sessao_login import SessaoLogin
from apresentacao.interface_inicial import InterfaceInicial


def main():
    # 1. Serviços Técnicos
    persistencia = PersistenciaJSON()

    # 2. Aplicação
    sessao_cadastro = SessaoCadastro(persistencia)
    sessao_login = SessaoLogin(persistencia)

    # 3. Apresentação (Ponto de entrada)
    app = InterfaceInicial(sessao_cadastro, sessao_login, persistencia)
    app.executar()


if __name__ == "__main__":
    main()