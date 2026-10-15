#!/usr/bin/env python3
"""
main.py
=======
Ponto de entrada interativo e executável do Projeto Atlas Access.
Sistema Baseado em Conhecimento (SBC) para Controle de Acesso a Áreas Industriais.

Instituição: Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe, São Carlos/SP
Curso: Pós-Graduação Lato Sensu em Inteligência Artificial
Equipe: Fábio, Fabi, Jonas Poli, Luciano
"""

import sys
import os
from typing import Optional

from engine.prolog_interpreter import PrologEngine
from engine.explanation_facility import explain_decision, CASES_METADATA
from engine.truth_table import format_truth_table_text
from src.state_machine import AccessRequestStateMachine, get_transition_table_data

HEADER = r"""
========================================================================================
   ____   _____  _        _    ____       _     ____ ____ _____ ____ ____  
  / ___| |_   _|/ \      / \  / ___|     / \   / ___/ ___| ____/ ___/ ___| 
  \___ \   | | / _ \    / _ \ \___ \    / _ \ | |  | |   |  _| \___ \___ \  
   ___) |  | |/ ___ \  / ___ \ ___) |  / ___ \| |__| |___| |___ ___) |__) | 
  |____/   |_/_/   \_\/_/   \_\____/  /_/   \_\\____\____|_____|____/____/  
  SISTEMA BASEADO EM CONHECIMENTO · CONTROLE DE ACESSO A ÁREAS INDUSTRIAIS
  Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe · São Carlos/SP
  Equipe: Fábio, Fabi, Jonas Poli, Luciano
========================================================================================
"""

def show_banner():
    print(HEADER)

def run_cases_matrix(engine: PrologEngine, include_c07: bool = True):
    status_label = "COM C07" if include_c07 else "SEM C07 (Apenas Base Original C01-C06)"
    print("\n" + "=" * 105)
    print(f"ETAPA 9: MATRIZ DE VALIDAÇÃO CRUZADA E TRILHA DE EXPLICAÇÃO [{status_label}]")
    print("=" * 105)
    header_fmt = "{:<5} | {:<22} | {:<25} | {:<16} | {:<15} | {:<12}"
    print(header_fmt.format("Caso", "Solicitação", "Regra Lógica", "Previsto", "Prolog (Obtido)", "Status FSM"))
    print("-" * 105)

    for case in CASES_METADATA:
        if case["id"] == "C07" and not include_c07:
            continue

        pessoa = case["pessoa"]
        area = case["area"]
        
        # Se C07 estiver ativo no engine, usa o engine diretamente
        proved, _, _ = engine.query(f"acesso({pessoa}, {area})")
        status_match = "COERENTE" if proved == case["resultado_esperado"] else "DIVERGENTE"
        fsm_state = "Autorizada" if proved else "Não autorizada"

        solicitacao = f"{pessoa.capitalize()} -> {area.capitalize()}"
        print(header_fmt.format(
            case["id"],
            solicitacao,
            case["regra_id"],
            str(case["resultado_esperado"]),
            str(proved),
            f"{fsm_state} [{status_match}]"
        ))
        print(f"      Regra:         {case['expressao_logica']}")
        print(f"      Fatos:         {case['fatos_sustentam']}")
        print(f"      Cond. Decisiva:{case['condicao_decisiva']}")
        print(f"      Justificativa: {case['justificativa']}")
        print("-" * 105)

def run_trace_analysis(engine: PrologEngine):
    print("\n" + "=" * 90)
    print("ETAPA 8: OBSERVAÇÃO DO MOTOR DE INFERÊNCIA (4 PORTAS: CALL / EXIT / FAIL / REDO)")
    print("=" * 90)
    
    # Caso 1: Sucesso (Ana / Produção)
    print("\n>>> CASO 1 (SUCESSO): acesso(ana, producao)")
    print("Objetivo: Provar elegibilidade de Ana para a Área de Produção via Regra R05.")
    res_ana, _, trace_ana = engine.query("acesso(ana, producao)", trace=True)
    print("-" * 75)
    for ev in trace_ana:
        print(ev)
    print("-" * 75)
    print("Análise do Sucesso:")
    print("1. Unificação: Constante 'ana' unifica com variável X em R05.")
    print("2. Ordem de busca: Objetivos avaliados da esquerda para a direita no corpo de R05.")
    print("3. Todos os 4 fatos (funcionario, credencial, treinamento, autorizacao) deram Exit.")
    print("4. Resultado final: True (Porta Exit na consulta principal).")

    # Caso 2: Falha e Backtracking (Diego / Produção)
    print("\n>>> CASO 2 (FALHA COM BACKTRACKING): acesso(diego, producao)")
    print("Objetivo: Investigar a tentativa de Diego para a Produção.")
    res_diego, _, trace_diego = engine.query("acesso(diego, producao)", trace=True)
    print("-" * 75)
    for ev in trace_diego:
        print(ev)
    print("-" * 75)
    print("Análise da Falha e Backtracking:")
    print("1. Tentativa 1: O motor tenta R05 (produção para funcionário) de cima para baixo.")
    print("2. Falha imediata: funcionario(diego) resulta em Fail.")
    print("3. Backtracking (Redo): O motor recua e busca a próxima cláusula compatível no arquivo: R06.")
    print("4. Tentativa 2: Em R06, prestador(diego), credencial e treinamento dão Exit com sucesso.")
    print("5. Falha crucial: autorizacao_especial(diego) resulta em Fail (condição ausente na base).")
    print("6. Não havendo mais alternativas no arquivo, o motor retorna Fail (false).")
    print("7. Conclusão sob a CWA: false significa 'não demonstrável com a base atual', e não prova de falsidade no mundo real.")

def run_state_machine_demo():
    print("\n" + "=" * 90)
    print("ETAPA 5: MÁQUINA DE ESTADOS DA SOLICITAÇÃO DE ACESSO")
    print("=" * 90)
    print("Diagrama de Estados (Mermaid / Conceitual):")
    print("""
       [Aguardando]
            |
            | (Solicitação recebida)
            v
       [Em análise] ----(Avaliação concluída SEM prova)----> [Não autorizada] (Terminal)
            |
            | (Avaliação concluída COM prova)
            v
       [Autorizada]
            |
            | (Entrada confirmada no sensor)
            v
    [Acesso em andamento]
            |
            | (Saída confirmada no sensor)
            v
     [Acesso encerrado] (Terminal)
    """)
    print("-" * 90)
    print("TABELA DE TRANSIÇÃO OFICIAL:")
    print("-" * 90)
    for row in get_transition_table_data():
        print(f"Estado Atual:    {row['estado_atual']}")
        print(f"Evento/Condição: {row['evento_condicao']}")
        print(f"Próximo Estado:  {row['proximo_estado']}")
        print(f"Ação Realizada:  {row['acao_justificativa']}")
        print("-" * 90)

    print("\nSIMULAÇÃO DE CICLO DE VIDA REAL (Ana -> Produção):")
    sm = AccessRequestStateMachine("Ana", "Área de Produção")
    print(f"1. Estado inicial: {sm.current_state.value}")
    sm.receive_request()
    print(f"2. Após envio da solicitação: {sm.current_state.value}")
    sm.evaluate_result(proved_in_kb=True, justification="Ana cumpre todos os requisitos da Regra R05.")
    print(f"3. Após inferência do SBC: {sm.current_state.value}")
    sm.confirm_entry()
    print(f"4. Após validação do giro de catraca: {sm.current_state.value}")
    sm.confirm_exit()
    print(f"5. Após saída da área: {sm.current_state.value} (Ciclo concluído com sucesso)")

def run_truth_table_demo():
    print(format_truth_table_text())

def run_evolution_demo():
    print("\n" + "=" * 90)
    print("ETAPA 10: EVOLUÇÃO DA BASE DE CONHECIMENTO")
    print("=" * 90)
    print("PARTE A: Alteração de um fato relevante")
    print("--------------------------------------------------------------------------------")
    print("Cenário: Bruno conclui o treinamento de segurança em conformidade com as normas.")
    print("Novo fato adicionado: treinamento_concluido(bruno).")
    print("Consulta: ?- acesso(bruno, laboratorio).")
    
    eng_orig = PrologEngine()
    eng_orig.load_file("src/atlas_access.pl")
    res_antes, _, _ = eng_orig.query("acesso(bruno, laboratorio)")
    print(f"  * Antes da evolução: {res_antes} (Não autorizado - falta treinamento em R03)")

    eng_evol = PrologEngine()
    eng_evol.load_file("src/atlas_access_evolucao.pl")
    res_depois, _, _ = eng_evol.query("acesso(bruno, laboratorio)")
    print(f"  * Após a evolução:   {res_depois} (AUTORIZADO com sucesso pela Regra R03!)")
    print(f"  * Transição FSM:     'Em análise' agora transita para 'Autorizada'.")

    print("\nPARTE B: Chegada de uma política nova (Regra R07)")
    print("--------------------------------------------------------------------------------")
    print("Comunicado da Segurança do Trabalho:")
    print("'A partir deste mês, prestadores de serviço com credencial válida e")
    print("treinamento concluído também podem acessar o Escritório Administrativo.'")
    print("Formalização lógica: (P ∧ C ∧ T) -> AE")
    print("Código adicionado (src/atlas_access_evolucao.pl):")
    print("""
    acesso(X, escritorio) :-
        prestador(X),
        credencial_valida(X),
        treinamento_concluido(X).
    """)
    res_diego_antes, _, _ = eng_orig.query("acesso(diego, escritorio)")
    res_diego_depois, _, _ = eng_evol.query("acesso(diego, escritorio)")
    print(f"  * Consulta: ?- acesso(diego, escritorio).")
    print(f"  * Na base original: {res_diego_antes} (Escritório era exclusivo de funcionários)")
    print(f"  * Na base evoluída: {res_diego_depois} (AUTORIZADO pela nova Regra R07!)")
    print("\nReflexão sobre Programação Declarativa:")
    print("  * Foram necessárias apenas 4 linhas de código.")
    print("  * NENHUMA linha de código anterior precisou ser modificada.")
    print("  * Isso demonstra o alto desacoplamento e a modularidade dos Sistemas Baseados em")
    print("    Conhecimento, contrastando com programas procedurais repletos de condicionais aninhadas.")

def run_c07_demo():
    print("\n" + "=" * 90)
    print("ETAPA 11: NOVO CASO CRIADO PELA EQUIPE (C07 - GUSTAVO)")
    print("=" * 90)
    print("Definição do perfil de Gustavo:")
    print("  * Categoria:          Funcionário (F)")
    print("  * Credencial válida:  Sim (C)")
    print("  * Treinamento:        Sim (T)")
    print("  * Autoriz. especial:  Não (sem S)")
    print("  * Fatos declarados:   funcionario(gustavo), credencial_valida(gustavo), treinamento_concluido(gustavo).")
    
    eng = PrologEngine()
    eng.load_file("src/atlas_access_evolucao.pl")

    print("\n1. Teste para o Laboratório Técnico:")
    print("   Consulta: ?- acesso(gustavo, laboratorio).")
    res_lab, _, trace_lab = eng.query("acesso(gustavo, laboratorio)", trace=True)
    print(f"   Resultado: {res_lab} (Autorizado pela Regra R03: F ∧ C ∧ T)")
    print("   Justificativa: Gustavo possui vínculo funcional, credencial e treinamento.")

    print("\n2. Teste para a Área de Produção:")
    print("   Consulta: ?- acesso(gustavo, producao).")
    res_prod, _, trace_prod = eng.query("acesso(gustavo, producao)", trace=True)
    print(f"   Resultado: {res_prod} (Não autorizado - Regra R05 exige autorização especial)")
    print("   Justificativa: Gustavo não possui autorização especial emitida pela Segurança do Trabalho.")

def interactive_query(engine: PrologEngine):
    print("\n" + "=" * 70)
    print("CONSULTA INTERATIVA DE ACESSO")
    print("=" * 70)
    print("Pessoas cadastradas: ana, bruno, carla, diego, elisa, fernando, gustavo")
    print("Áreas disponíveis:  recepcao, escritorio, laboratorio, producao")
    pessoa = input("Digite o nome da pessoa: ").strip().lower()
    area = input("Digite a área desejada:  ").strip().lower()

    if not pessoa or not area:
        print("Entrada inválida.")
        return

    # Se for gustavo, usa a base evoluída
    eng = engine
    if pessoa == "gustavo":
        eng = PrologEngine()
        eng.load_file("src/atlas_access_evolucao.pl")

    decision = explain_decision(pessoa, area, eng)
    print("\n" + "=" * 70)
    print(f"RESULTADO: {'AUTORIZADO' if decision['resultado'] else 'NÃO AUTORIZADO'}")
    print(f"Regra Aplicada / Analisada: {decision['regra']} ({decision['formula']})")
    print(f"Fatos Encontrados:          {decision['fatos']}")
    print(f"Estado FSM Resultante:      {decision['estado']}")
    print(f"Justificativa ao Usuário:   {decision['justificativa']}")
    print("=" * 70)

def main():
    engine = PrologEngine()
    engine.load_file("src/atlas_access.pl")

    # Modos não interativos via flag
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--all", "-a"]:
            show_banner()
            run_cases_matrix(engine)
            run_trace_analysis(engine)
            run_state_machine_demo()
            run_truth_table_demo()
            run_evolution_demo()
            run_c07_demo()
            return
        elif arg in ["--test", "-t"]:
            import unittest
            from tests.test_suite import TestAtlasAccessOriginal, TestAtlasAccessEvolucao, TestStateMachine, TestTruthTable
            suite = unittest.TestSuite()
            for cls in [TestAtlasAccessOriginal, TestAtlasAccessEvolucao, TestStateMachine, TestTruthTable]:
                suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
            return
        elif arg in ["--matrix", "-m"]:
            run_cases_matrix(engine)
            return
        elif arg in ["--trace"]:
            run_trace_analysis(engine)
            return
        elif arg in ["--table"]:
            run_truth_table_demo()
            return

    show_banner()
    while True:
        c07_status = "ATIVADO (Gustavo na base)" if engine.is_c07_active() else "DESATIVADO (Base original C01-C06)"
        print("\nMENU PRINCIPAL - PROJETO ATLAS ACCESS:")
        print(f"  [T] ATIVAR / DESATIVAR Caso C07 (Gustavo) -> [Status Atual: {c07_status}]")
        print("  1. Matriz de Validação Cruzada dos Casos")
        print("  2. Análise do Motor de Inferência e Trace 4-Portas (Ana vs Diego)")
        print("  3. Simulação da Máquina de Estados (Diagrama e Transições)")
        print("  4. Tabela-Verdade Completa de 32 Linhas da Regra R05")
        print("  5. Demonstração da Evolução da Base (Etapa 10 Partes A e B)")
        print("  6. Demonstração do Caso Criado C07 (Gustavo - Etapa 11)")
        print("  7. Consulta Interativa de Acesso com Justificativa")
        print("  8. Executar Suíte de Testes Automatizados")
        print("  9. Executar Todas as Demonstrações Completas (--all)")
        print("  0. Sair")
        try:
            choice = input("\nEscolha uma opção (0-9 ou T): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o Sistema Atlas Access.")
            break

        if choice.upper() == "T":
            if engine.is_c07_active():
                engine.deactivate_c07()
                print("\n>>> CASO C07 DESATIVADO: Gustavo foi removido da base de conhecimento!")
            else:
                engine.activate_c07()
                print("\n>>> CASO C07 ATIVADO: Gustavo foi cadastrado na base (F=1, C=1, T=1, S=0)!")
        elif choice == "1":
            run_cases_matrix(engine, include_c07=engine.is_c07_active())
        elif choice == "2":
            run_trace_analysis(engine)
        elif choice == "3":
            run_state_machine_demo()
        elif choice == "4":
            run_truth_table_demo()
        elif choice == "5":
            run_evolution_demo()
        elif choice == "6":
            run_c07_demo()
        elif choice == "7":
            interactive_query(engine)
        elif choice == "8":
            os.system("python3 -m unittest tests/test_suite.py")
        elif choice == "9":
            run_cases_matrix(engine, include_c07=True)
            run_trace_analysis(engine)
            run_state_machine_demo()
            run_truth_table_demo()
            run_evolution_demo()
            run_c07_demo()
        elif choice == "0":
            print("\nEncerrando o Sistema Atlas Access. Obrigado!\n")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
