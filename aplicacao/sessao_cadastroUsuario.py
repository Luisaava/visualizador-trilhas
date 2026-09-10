from dominio.usuarios import Usuario
from servicos_tecnicos.persistencia import PersistenciaJSON


class SessaoCadastro:
    def __init__(self, persistencia: PersistenciaJSON):
        self.persistencia = persistencia

    def criar_usuario(self, nome: str, senha: str) -> tuple[bool, Usuario | None, str]:
        if not nome.strip() or not senha.strip():
            return False, None, "Erro: Nome e senha são obrigatórios."

        usuarios = self.persistencia.carregar_todos()
        if nome in usuarios:
            return False, None, f"Erro: O usuário '{nome}' já existe."

        novo_usuario = Usuario(nome, senha)
        usuarios[nome] = novo_usuario
        self.persistencia.salvar_todos(usuarios)

        return True, novo_usuario, f"Usuário '{nome}' cadastrado com sucesso!"