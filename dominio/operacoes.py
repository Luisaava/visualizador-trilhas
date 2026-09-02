from dataclasses import dataclass

@dataclass
class Calculo:
    operando1: float
    operador: str
    operando2: float
    resultado: float
    data_hora: str = None


class OperacoesMatematicas:
    @staticmethod
    def executar(op1: float, operador: str, op2: float) -> float:
        if operador == '+':
            return op1 + op2
        elif operador == '-':
            return op1 - op2
        elif operador == '*':
            return op1 * op2
        elif operador == '/':
            if op2 == 0:
                raise ValueError("Erro: Divisão por zero não é permitida.")
            return op1 / op2
        else:
            raise ValueError(f"Operador '{operador}' inválido. Use +, -, * ou /.")