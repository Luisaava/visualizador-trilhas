import sqlite3
from dominio.operacoes import Calculo

class PersistenciaHistorico:
    def __init__(self, db_path="calculadora.db"):
        self.db_path = db_path
        self._criar_tabela()

    def _criar_tabela(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operando1 REAL,
                    operador TEXT,
                    operando2 REAL,
                    resultado REAL,
                    data_hora TEXT
                )
            """)
            conn.commit()

    def salvar(self, calculo: Calculo):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO historico (operando1, operador, operando2, resultado, data_hora)
                VALUES (?, ?, ?, ?, ?)
            """, (calculo.operando1, calculo.operador, calculo.operando2, calculo.resultado, calculo.data_hora))
            conn.commit()

    def listar_todos(self) -> list[Calculo]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT operando1, operador, operando2, resultado, data_hora FROM historico ORDER BY id DESC"
            )
            linhas = cursor.fetchall()
            return [Calculo(op1, op, op2, res, dt) for op1, op, op2, res, dt in linhas]