from datetime import datetime
from dominio.operacoes import Calculo, OperacoesMatematicas
from servicos_tecnicos.persistencia import PersistenciaHistorico

class SessaoCalculo:
    def __init__(self, repositorio: PersistenciaHistorico):
        self.repositorio = repositorio

    def realizar_calculo(self, op1: float, operador: str, op2: float) -> Calculo:
        resultado = OperacoesMatematicas.executar(op1, operador, op2)
        data_agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        calculo = Calculo(op1, operador, op2, resultado, data_agora)
        self.repositorio.salvar(calculo)
        return calculo

    def obter_historico(self) -> list[Calculo]:
        return self.repositorio.listar_todos()