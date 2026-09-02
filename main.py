from servicos_tecnicos.persistencia import PersistenciaHistorico
from aplicacao.sessao_calculo import SessaoCalculo
from apresentacao.interface_calculadora import InterfaceCalculadora

if __name__ == "__main__":
    repositorio = PersistenciaHistorico()
    servico_aplicacao = SessaoCalculo(repositorio)
    interface = InterfaceCalculadora(servico_aplicacao)
    interface.exibir_menu()