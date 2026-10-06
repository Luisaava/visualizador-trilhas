import json
import os
from dominio.usuarios import Usuario


class PersistenciaJSON:
    def __init__(self, arquivo: str = "usuarios.json"):
        self.arquivo = arquivo

    def carregar_todos(self) -> dict[str, Usuario]: #vai ser bom utilizar quando for listar usuarios e tambem quando buscar algum especifico
        if not os.path.exists(self.arquivo):
            return {}
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return {nome: Usuario.from_dict(info) for nome, info in dados.items()}
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def salvar_todos(self, usuarios: dict[str, Usuario]) -> None: #funcao padrao de salvar no json
        dados = {nome: user.to_dict() for nome, user in usuarios.items()}
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)