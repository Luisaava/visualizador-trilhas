from aplicacao import sessao_login
from dominio.usuarios import Usuario

def telaLogin() -> Usuario:
    while True:
        usuario: str = input("Insira seu nome de usuário ou digite \'sair\' para sair: ")
        if usuario == 'sair': break
        senha: str = input("Digite sua senha: ")
        login: tuple[bool,Usuario] = sessao_login.realizarLogin(usuario, senha)
        if login[0]:
            return login[1]

def criarUsuario() -> Usuario:
    while True:
        usuario: str = input("Insira seu nome de usuário ou digite \'sair\' para sair: ")
        if usuario == 'sair': break
        senha: str = input("Digite sua senha: ")
        usuarioCriado: tuple[bool,Usuario] = sessao_login.criarUsuario(usuario, senha)
        if usuarioCriado[0]:
            return usuarioCriado[1]