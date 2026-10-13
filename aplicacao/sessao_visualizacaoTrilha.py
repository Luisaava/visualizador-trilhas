from dominio.trilhas import trilhas, Trilha

class SessaoVisualizacaoTrilha:
    def __init__(self):
        pass

    def exibir_trilhas(self) -> Trilha | None:
        lista_trilhas = list(trilhas.values())
        
        if not lista_trilhas:
            print("\nNenhuma trilha disponível no momento.")
            return None
        
        print("\n=== Trilhas Disponíveis ===")
        for i, trilha in enumerate(lista_trilhas, start=1):
            print(f"{i} - {trilha.nome} (Dificuldade: {trilha.dificuldade}, Duração média: {trilha.duracaoMedia})")
        
        escolha = input("\nEscolha o número da trilha que deseja ver/cursar (ou 0 para voltar): ").strip()
        
        if escolha == '0':
            return None
            
        if escolha.isdigit() and 1 <= int(escolha) <= len(lista_trilhas):
            trilha_escolhida = lista_trilhas[int(escolha) - 1]
            
            print("\n" + "="*40)
            print(f"DETALHES DA TRILHA: {trilha_escolhida.nome}")
            print("="*40)
            print(f"📍 Início: {trilha_escolhida.localInicio}")
            print(f"🏁 Fim: {trilha_escolhida.localFim}")
            print(f"⚠️ Dificuldade (1-10): {trilha_escolhida.dificuldade}")
            print(f"📏 Comprimento: {trilha_escolhida.comprimento} km")
            print(f"⛰️ Variação de Altitude: {trilha_escolhida.variacaoAltitude}m")
            print(f"⏱️ Duração Média: {trilha_escolhida.duracaoMedia}")
            print(f"👤 Criada por: {trilha_escolhida.criador.nome}")
            print("="*40 + "\n")
            
            return trilha_escolhida
        else:
            print("\nOpção inválida.")
            return None