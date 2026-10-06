from dominio.usuarios import Usuario
from servicos_tecnicos.persistencia import PersistenciaJSON

MOD_USUARIO = "moderador"
MOD_SENHA = "123"


class SessaoLogin:
    def __init__(self, persistencia: PersistenciaJSON):
        self.persistencia = persistencia

    def autenticar(self, nome: str, senha: str) -> tuple[bool, str, Usuario | None]:
        """
        Retorna: (sucesso, tipo_sessao, objeto_usuario)
        tipo_sessao pode ser: 'MODERADOR', 'USUARIO' ou ''
        """
        if nome == MOD_USUARIO and senha == MOD_SENHA:
            return True, "MODERADOR", None

        usuarios = self.persistencia.carregar_todos()
        usuario = usuarios.get(nome)
        if usuario and usuario.senha == senha:
            return True, "USUARIO", usuario

        return False, "", None