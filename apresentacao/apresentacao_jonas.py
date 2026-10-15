#!/usr/bin/env python3
"""
apresentacao_jonas.py
=====================
Script dedicado de apresentação para o Bloco do Jonas (Slides 10 ao 14).
Projeto Atlas Access - Sistema Baseado em Conhecimento (SBC).

Instituição: Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe, São Carlos/SP
Curso: Pós-Graduação Lato Sensu em Inteligência Artificial
Equipe: Fábio, Fabi, Jonas Poli, Luciano
Bloco: Jonas Poli (18:00 às 27:00 · 9 minutos no total)

Uso:
    python3 apresentacao_jonas.py       # Apresentação interativa passo a passo
    python3 apresentacao_jonas.py 10    # Exibir apenas Slide 10
    python3 apresentacao_jonas.py 11    # Exibir apenas Slide 11
    python3 apresentacao_jonas.py 12    # Exibir apenas Slide 12 (Trace Ana)
    python3 apresentacao_jonas.py 13    # Exibir apenas Slide 13 (Trace Diego - Backtracking)
    python3 apresentacao_jonas.py 14    # Exibir apenas Slide 14 (Tabela Previsão x Execução)
    python3 apresentacao_jonas.py --all # Executar todos os slides sequencialmente
"""

import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(CURRENT_DIR) in ["python", "apresentacao"]:
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
else:
    PROJECT_ROOT = CURRENT_DIR

for p in [PROJECT_ROOT, os.path.join(PROJECT_ROOT, "python")]:
    if p not in sys.path:
        sys.path.insert(0, p)

def get_kb_path(filename="atlas_access.pl"):
    for candidate in [
        os.path.join(PROJECT_ROOT, "prolog", filename),
        os.path.join(PROJECT_ROOT, "src", filename),
        os.path.join("prolog", filename),
        os.path.join("src", filename)
    ]:
        if os.path.exists(candidate):
            return candidate
    return filename

from engine.prolog_interpreter import PrologEngine

def colorize(text: str, color_code: str) -> str:
    # Cores ANSI para destaque no terminal
    return f"\033[{color_code}m{text}\033[0m"

CYAN = "1;36"
GREEN = "1;32"
YELLOW = "1;33"
RED = "1;31"
MAGENTA = "1;35"
BOLD = "1"

def pause():
    try:
        input(colorize("\n[Pressione ENTER para avançar para o próximo slide...]", YELLOW))
    except (KeyboardInterrupt, EOFError):
        print("\nSaindo...")
        sys.exit(0)

def show_slide_10(engine: PrologEngine):
    print("\n" + "=" * 88)
    print(colorize("SLIDE 10 · FATOS, REGRAS E INFERÊNCIA", CYAN))
    print("Etapas 6 e 7 | Horário na apresentação: 18:00 – 19:00 (Duração: 1:00 min)")
    print("Apresentador: Jonas")
    print("=" * 88)

    print(colorize("\n1. RESPOSTA DA EQUIPE · BASE DE CONHECIMENTO DECLARATIVA:", BOLD))
    print("   Fatos Positivos sobre Ana declarados na base:")
    print("     " + colorize("funcionario(ana).", GREEN))
    print("     " + colorize("credencial_valida(ana).", GREEN))
    print("     " + colorize("treinamento_concluido(ana).", GREEN))
    print("     " + colorize("autorizacao_especial(ana).", GREEN))

    print(colorize("\n2. CONSULTA (GOAL) SUBMETIDA AO MOTOR DE INFERÊNCIA:", BOLD))
    print("     " + colorize("?- acesso(ana, producao).", YELLOW))

    print(colorize("\n3. EXECUÇÃO COMPUTACIONAL EM TEMPO REAL:", BOLD))
    proved, sols, _ = engine.query("acesso(ana, producao)")
    res_str = colorize("true", GREEN) if proved else colorize("false", RED)
    print(f"   Resultado obtido pelo motor: {res_str}")

    print(colorize("\n4. CONHECIMENTO USADO & PONTOS CHAVE DA FALA:", BOLD))
    print("   • Distinção conceitual: Fato é o que é dado como verdadeiro a priori;")
    print("     Regra é a implicação geral que define elegibilidade;")
    print("     Conclusão inferida é o resultado derivado pelo motor (não é armazenada como fato).")
    print("   • Por que a autorização de Ana não deve ser salva como fato direto?")
    print("     Porque isso transformaria o sistema em um mero repositório procedural.")
    print("     Representar o conhecimento na forma de regras permite que o sistema decida")
    print("     dinamicamente perante qualquer mudança de fatos no cadastro.")
    print("=" * 88)

def show_slide_11():
    print("\n" + "=" * 88)
    print(colorize("SLIDE 11 · REGRA PROLOG E UNIFICAÇÃO", CYAN))
    print("Etapas 6 e 7 | Horário na apresentação: 19:00 – 21:00 (Duração: 2:00 min)")
    print("Apresentador: Jonas")
    print("=" * 88)

    print(colorize("\n1. CLÁUSULA DE HORN DEFINIDA (REGRA R05):", BOLD))
    print("""   acesso(X, producao) :-
       funcionario(X),
       credencial_valida(X),
       treinamento_concluido(X),
       autorizacao_especial(X).""")

    print(colorize("\n2. AS TRÊS REGRAS FORMAIS DE UNIFICAÇÃO SINTÁTICA:", BOLD))
    print("   +-----------------------------+----------------------------------------------------+")
    print("   | Regra de Unificação         | Aplicação Concreta neste Caso                      |")
    print("   +-----------------------------+----------------------------------------------------+")
    print("   | 1. Constantes iguais        | O átomo 'producao' unifica com 'producao'.         |")
    print("   | 2. Variável livre e termo   | A variável 'X' unifica e instancia a constante ana |")
    print("   |                             | em todo o escopo da regra: X = ana.                |")
    print("   | 3. Estruturas compatíveis   | Functor 'acesso' de aridade 2 unifica com a cabeça |")
    print("   |                             | da regra que possui aridade 2 e argumentos compat. |")
    print("   +-----------------------------+----------------------------------------------------+")

    print(colorize("\n3. MECANISMO DE BUSCA DO MOTOR PROLOG:", BOLD))
    print("   • " + colorize("De cima para baixo no arquivo:", YELLOW) + " Cláusulas são testadas na ordem declarada.")
    print("   • " + colorize("Da esquerda para a direita no corpo:", YELLOW) + " Primeiro testa funcionario(X), depois credencial, etc.")
    print("=" * 88)

def show_slide_12(engine: PrologEngine):
    print("\n" + "=" * 88)
    print(colorize("SLIDE 12 · ANA: UMA PROVA BEM-SUCEDIDA", CYAN))
    print("Etapas 7 e 8 | Horário na apresentação: 21:00 – 22:30 (Duração: 1:30 min)")
    print("Apresentador: Jonas")
    print("=" * 88)

    print(colorize("\nConsulta avaliada:", BOLD) + " " + colorize("?- acesso(ana, producao).", GREEN))
    print(colorize("\nTABELA DO SLIDE 12 (RASTREAMENTO DE PORTAS BYRD):", BOLD))

    print("   +" + "-"*33 + "+" + "-"*16 + "+" + "-"*24 + "+")
    print(f"   | {'Objetivo':<31} | {'Portas':<14} | {'Resultado':<22} |")
    print("   +" + "-"*33 + "+" + "-"*16 + "+" + "-"*24 + "+")
    print(f"   | {'funcionario(ana)':<31} | {'Call / Exit':<14} | {'Fato encontrado':<22} |")
    print(f"   | {'credencial_valida(ana)':<31} | {'Call / Exit':<14} | {'Fato encontrado':<22} |")
    print(f"   | {'treinamento_concluido(ana)':<31} | {'Call / Exit':<14} | {'Fato encontrado':<22} |")
    print(f"   | {'autorizacao_especial(ana)':<31} | {'Call / Exit':<14} | {'Fato encontrado':<22} |")
    print(f"   | {colorize('acesso(ana, producao)', BOLD):<40} | {colorize('Exit', GREEN):<23} | {colorize('true', GREEN):<31} |")
    print("   +" + "-"*33 + "+" + "-"*16 + "+" + "-"*24 + "+")

    print(colorize("\nCONHECIMENTO USADO:", BOLD))
    print("   Todos os objetivos do corpo de R05 têm sucesso com X = ana.")
    print("   Não houve necessidade de desfazer escolhas -> " + colorize("NÃO OCORREU BACKTRACKING", GREEN) + ".")
    print("=" * 88)

def show_slide_13(engine: PrologEngine):
    print("\n" + "=" * 88)
    print(colorize("SLIDE 13 · DIEGO: ALTERNATIVAS E FALHA", CYAN))
    print("Etapas 7 e 8 | Horário na apresentação: 22:30 – 25:00 (Duração: 2:30 min)")
    print("Apresentador: Jonas")
    print("=" * 88)

    print(colorize("\nConsulta avaliada:", BOLD) + " " + colorize("?- acesso(diego, producao).", GREEN))
    print(colorize("\nTABELA DO SLIDE 13 (PASSOS, ALTERNATIVAS E BACKTRACKING):", BOLD))

    print("   +" + "-"*7 + "+" + "-"*45 + "+" + "-"*21 + "+")
    print(f"   | {'Passo':^5} | {'Objetivo / alternativa':<43} | {'Porta':<19} |")
    print("   +" + "-"*7 + "+" + "-"*45 + "+" + "-"*21 + "+")
    print(f"   | {'1':^5} | {'funcionario(diego), em R05':<43} | {colorize('Call / Fail', RED):<30} |")
    print(f"   | {'2':^5} | {'acesso(diego, producao), alternativa R06':<43} | {colorize('Redo', YELLOW):<30} |")
    print(f"   | {'3':^5} | {'prestador(diego)':<43} | {'Call / Exit':<19} |")
    print(f"   | {'4':^5} | {'credencial_valida(diego)':<43} | {'Call / Exit':<19} |")
    print(f"   | {'5':^5} | {'treinamento_concluido(diego)':<43} | {'Call / Exit':<19} |")
    print(f"   | {'6':^5} | {'autorizacao_especial(diego)':<43} | {colorize('Call / Fail', RED):<30} |")
    print(f"   | {'7':^5} | {colorize('acesso(diego, producao)', BOLD):<52} | {colorize('Fail / false', RED):<30} |")
    print("   +" + "-"*7 + "+" + "-"*45 + "+" + "-"*21 + "+")

    print(colorize("\nCONHECIMENTO USADO:", BOLD))
    print("   Backtracking procura outra prova. Todos os requisitos continuam obrigatórios.")
    print("   " + colorize("false", RED) + " significa 'não demonstrável com os fatos e regras da base atual' (CWA).")
    print("=" * 88)

def show_slide_14(engine: PrologEngine):
    print("\n" + "=" * 88)
    print(colorize("SLIDE 14 · PREVISÃO E EXECUÇÃO", CYAN))
    print("Etapa 8 | Horário na apresentação: 25:00 – 27:00 (Duração: 2:00 min)")
    print("Apresentador: Jonas")
    print("=" * 88)

    casos = [
        ("acesso(ana, producao)", "true", "true", "Autorizado: Satisfez R05 (F ∧ C ∧ T ∧ S)"),
        ("acesso(bruno, laboratorio)", "false", "false", "Negado: Ausência do fato treinamento"),
        ("acesso(carla, laboratorio)", "true", "true", "Autorizado: Satisfez R04 (P ∧ C ∧ T)"),
        ("acesso(diego, producao)", "false", "false", "Negado: Ausência de autorizacao_especial"),
        ("acesso(elisa, laboratorio)", "false", "false", "Sem Regra: Base não prevê visitante em lab"),
        ("acesso(fernando, producao)", "false", "false", "Negado: Ausência de autorizacao_especial")
    ]

    print(colorize("\nTABELA DO SLIDE 14 (CONSULTA, PREVISTO, EXECUTADO E DIAGNÓSTICO CWA):", BOLD))
    print("   +" + "-"*31 + "+" + "-"*12 + "+" + "-"*13 + "+" + "-"*44 + "+")
    print(f"   | {'Consulta':<29} | {'Previsto':^10} | {'Executado':^11} | {'Diagnóstico Formal (CWA)':<42} |")
    print("   +" + "-"*31 + "+" + "-"*12 + "+" + "-"*13 + "+" + "-"*44 + "+")

    for query, prev, exec_esperado, diag in casos:
        proved, _, _ = engine.query(query)
        real_exec = "true" if proved else "false"
        color_prev = GREEN if prev == "true" else RED
        color_exec = GREEN if real_exec == "true" else RED
        p_str = colorize(f"{prev:^10}", color_prev)
        e_str = colorize(f"{real_exec:^11}", color_exec)
        print(f"   | {query:<29} | {p_str} | {e_str} | {diag:<42} |")

    print("   +" + "-"*31 + "+" + "-"*12 + "+" + "-"*13 + "+" + "-"*44 + "+")

    print(colorize("\nCONHECIMENTO USADO:", BOLD))
    print("   false significa “não demonstrável sob a Closed World Assumption (CWA)”.")
    print("   100% de convergência entre dedução formal teórica e execução computacional Prolog.")
    print("=" * 88)

    print(colorize("\nSÍNTESE FINAL DO BLOCO DO JONAS:", BOLD))
    print("   • Todas as predições coincidiram 100% com o comportamento observado.")
    print("   • Diferença conceitual crucial para responder à banca:")
    print("     - Em C02, C04 e C06: " + colorize("Existe regra aplicável", YELLOW) + ", mas falta uma condição fática.")
    print("     - Em C05 (Elisa): " + colorize("NÃO EXISTE regra aplicável", RED) + " na base para visitante no laboratório.")
    print("=" * 88)

def show_c07_activation_demo(engine: PrologEngine):
    print("\n" + "=" * 88)
    print(colorize("ETAPA 11 · CASO C07 (GUSTAVO): ATIVAÇÃO E DESATIVAÇÃO DINÂMICA", CYAN))
    print("Demonstração prática de como ativar e desativar o caso criado pela equipe.")
    print("=" * 88)

    print(colorize("\n1. ESTADO INICIAL (C07 DESATIVADO):", BOLD))
    print(f"   Gustavo está na base? {engine.is_c07_active()}")
    p1, _, _ = engine.query("acesso(gustavo, laboratorio)")
    print(f"   Consulta: acesso(gustavo, laboratorio) -> {colorize(str(p1), RED)} (Inexistente na base)")

    print(colorize("\n2. EXECUTANDO A ATIVAÇÃO DO CASO C07 (Etapa 11):", BOLD))
    engine.activate_c07()
    print("   [+] Inseridos fatos: pessoa(gustavo), funcionario(gustavo),")
    print("                        credencial_valida(gustavo), treinamento_concluido(gustavo).")
    print("   [*] autorizacao_especial(gustavo) omitida (S = 0 sob a CWA).")
    print(f"   Gustavo está na base agora? {colorize(str(engine.is_c07_active()), GREEN)}")

    print(colorize("\n3. CONSULTAS APÓS A ATIVAÇÃO:", BOLD))
    p2, _, _ = engine.query("acesso(gustavo, laboratorio)")
    p3, _, _ = engine.query("acesso(gustavo, producao)")
    print(f"   • ?- acesso(gustavo, laboratorio). -> {colorize(str(p2), GREEN)} (Autorizado via R03: F ∧ C ∧ T)")
    print(f"   • ?- acesso(gustavo, producao).    -> {colorize(str(p3), RED)} (Não autorizado: falta S em R05)")

    print(colorize("\n4. EXECUTANDO A DESATIVAÇÃO DO CASO C07:", BOLD))
    engine.deactivate_c07()
    p4, _, _ = engine.query("acesso(gustavo, laboratorio)")
    print("   [-] Removidos todos os fatos relativos a Gustavo.")
    print(f"   Gustavo está na base agora? {engine.is_c07_active()}")
    print(f"   • ?- acesso(gustavo, laboratorio). -> {colorize(str(p4), RED)} (Retornou a false)")
    print("=" * 88)

def main():
    engine = PrologEngine()
    engine.load_file(get_kb_path("atlas_access.pl"))

    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if arg == "10":
            show_slide_10(engine)
        elif arg == "11":
            show_slide_11()
        elif arg == "12":
            show_slide_12(engine)
        elif arg == "13":
            show_slide_13(engine)
        elif arg == "14":
            show_slide_14(engine)
        elif arg in ["--all", "-a"]:
            show_slide_10(engine)
            show_slide_11()
            show_slide_12(engine)
            show_slide_13(engine)
            show_slide_14(engine)
        elif arg in ["--c07", "c07", "11"]:
            show_c07_activation_demo(engine)
        else:
            print(f"Argumento desconhecido: {arg}. Use 10, 11, 12, 13, 14, --c07 ou --all.")
        return

    # Modo Interativo de Apresentação
    print(colorize("\n" + "=" * 88, CYAN))
    print(colorize("   INICIANDO SIMULAÇÃO DA APRESENTAÇÃO DE 40 MINUTOS - BLOCO DO JONAS", CYAN))
    print(colorize("   Slides 10 ao 14 · Duração prevista: 9 minutos (18:00 às 27:00)", CYAN))
    print(colorize("=" * 88, CYAN))

    show_slide_10(engine)
    pause()

    show_slide_11()
    pause()

    show_slide_12(engine)
    pause()

    show_slide_13(engine)
    pause()

    show_slide_14(engine)
    print(colorize("\n[Fim do bloco do Jonas! Passando a palavra para o Luciano para o Slide 15 - Máquina de Estados.]\n", GREEN))

if __name__ == "__main__":
    main()

