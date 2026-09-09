from dominio.usuarios import Usuario, usuarios
def realizarLogin (usuario: str, senha: str) -> tuple[bool, Usuario]:
    usuarioBD = usuarios.get(usuario)
    if usuarioBD and usuarioBD.senha == senha:
        print(f'Usuário {usuarioBD.nome} autenticado.')
        return True, usuarioBD
    print("Erro: login e senha inconsistentes.")
    return False, None

def criarUsuario (nome:str, senha:str) -> tuple[bool, Usuario]:
    if not usuarios[nome]:
        usuarios[nome] = Usuario(nome, senha)
        print(f'Usuário {nome} criado.')
        return True, usuarios[nome]
    print(f'Erro: usuário com nome {nome} já existente.')
    return False, None