from servicos_tecnicos.persistencia import PersistenciaJSON
from aplicacao.sessao_cadastroUsuario import SessaoCadastro
from aplicacao.sessao_login import SessaoLogin
from apresentacao.interface_inicial import InterfaceInicial

from dominio.usuarios import Usuario
from dominio.trilhas import Trilha, trilhas
from datetime import time

# def carregar_trilhas_teste():
#     usuario_teste = Usuario(nome="AdminTeste", senha="123")

#     trilha_falsa_1 = Trilha(
#         nome="Trilha da Costa da Lagoa",
#         inicio="Canto dos Araçás",
#         fim="Centrinho da Costa",
#         dif=4,
#         comprimento=7.5,
#         alturaMin=0,
#         alturaMax=150,
#         tempoMedio=time(2, 30, 0),
#         usuario=usuario_teste
#     )

#     trilha_falsa_2 = Trilha(
#         nome="Trilha do Gravatá",
#         inicio="Praia Mole",
#         fim="Praia do Gravatá",
#         dif=3,
#         comprimento=1.2,
#         alturaMin=0,
#         alturaMax=60,
#         tempoMedio=time(0, 45, 0),
#         usuario=usuario_teste
#     )

#     trilhas[trilha_falsa_1.nome] = trilha_falsa_1
#     trilhas[trilha_falsa_2.nome] = trilha_falsa_2

def main():

    # Serviços Técnicos
    persistencia = PersistenciaJSON()

    #Aplicação
    sessao_cadastro = SessaoCadastro(persistencia)
    sessao_login = SessaoLogin(persistencia)

    #Apresentação
    app = InterfaceInicial(sessao_cadastro, sessao_login, persistencia)
    app.executar()


if __name__ == "__main__":
    main()