"""
engine/truth_table.py
=====================
Gera e analisa a tabela-verdade completa de 32 linhas para a regra R05:
(F ∧ C ∧ T ∧ S) -> AP

Demonstra:
- Em quantas linhas o antecedente H é verdadeiro (2 linhas).
- Em quantas linhas a implicação inteira é verdadeira (31 linhas).
- Em qual linha a implicação é falsa (1 linha: H=1 e AP=0).
- Significado semântico e prático de uma linha em que H=0 e H->AP=1 (verdade vacínua).
"""

from typing import List, Dict, Any

def generate_r05_truth_table() -> List[Dict[str, Any]]:
    rows = []
    # 5 proposições: F, C, T, S, AP -> 2^5 = 32 linhas
    row_num = 1
    for f in [1, 0]:
        for c in [1, 0]:
            for t in [1, 0]:
                for s in [1, 0]:
                    for ap in [1, 0]:
                        h = f & c & t & s
                        implication = 0 if (h == 1 and ap == 0) else 1
                        
                        if h == 1 and ap == 1:
                            interp = "Condições satisfeitas e acesso concedido (Modus Ponens válido)"
                        elif h == 1 and ap == 0:
                            interp = "VIOLAÇÃO DA REGRA (Premissas atendidas, mas acesso barrado)"
                        elif h == 0 and ap == 1:
                            interp = "Antecedente falso; implicação vacilamente verdadeira (não autoriza)"
                        else:
                            interp = "Antecedente falso e sem acesso; implicação consistente (sem prova)"

                        rows.append({
                            "num": row_num,
                            "F": f,
                            "C": c,
                            "T": t,
                            "S": s,
                            "AP": ap,
                            "H": h,
                            "impl": implication,
                            "interp": interp
                        })
                        row_num += 1
    return rows

def format_truth_table_text() -> str:
    rows = generate_r05_truth_table()
    out = []
    out.append("=" * 95)
    out.append("TABELA-VERDADE COMPLETA DA REGRA R05: (F ∧ C ∧ T ∧ S) -> AP")
    out.append("H = F ∧ C ∧ T ∧ S  |  1: Verdadeiro, 0: Falso  |  Total de Linhas: 32")
    out.append("=" * 95)
    out.append(f"{'Nº':^4} | {'F':^3} | {'C':^3} | {'T':^3} | {'S':^3} | {'AP':^3} | {'H':^3} | {'H->AP':^5} | {'Interpretação Semântica Operacional'}")
    out.append("-" * 95)
    for r in rows:
        out.append(f"{r['num']:^4} | {r['F']:^3} | {r['C']:^3} | {r['T']:^3} | {r['S']:^3} | {r['AP']:^3} | {r['H']:^3} | {r['impl']:^5} | {r['interp']}")
    out.append("=" * 95)

    h_true_count = sum(1 for r in rows if r['H'] == 1)
    impl_true_count = sum(1 for r in rows if r['impl'] == 1)
    impl_false_count = sum(1 for r in rows if r['impl'] == 0)

    out.append("\nANÁLISE QUANTITATIVA E SEMÂNTICA:")
    out.append(f"1. Linhas em que o antecedente (H) é verdadeiro: {h_true_count} de 32 (apenas linhas 1 e 2).")
    out.append(f"2. Linhas em que a implicação completa (H -> AP) é verdadeira: {impl_true_count} de 32.")
    out.append(f"3. Linhas em que a implicação completa é falsa: {impl_false_count} de 32 (Linha 2: H=1 e AP=0).")
    out.append("\nRESPOSTA À PERGUNTA FUNDAMENTAL DA ETAPA 3:")
    out.append("O que significa, do ponto de vista da política de acesso, uma linha em que o antecedente é falso e a implicação é verdadeira?")
    out.append("-" * 95)
    out.append("RESPOSTA: Na lógica clássica, a implicação material P -> Q é definida como ¬P ∨ Q. Por isso, quando o antecedente")
    out.append("P é falso, a sentença inteira é formalmente verdadeira por vacuidade (verdade vacínua).")
    out.append("Contudo, DO PONTO DE VISTA OPERACIONAL DO SBC, ISSO NÃO SIGNIFICA QUE O ACESSO ESTÁ LIBERADO!")
    out.append("Para autorizar uma ação ou deduzir que Q é verdadeiro através de uma regra P -> Q, o motor de inferência precisa")
    out.append("aplicar a regra de inferência MODUS PONENS:")
    out.append("       Premissa 1: P -> Q")
    out.append("       Premissa 2: P")
    out.append("       Conclusão:  Q")
    out.append("Se o antecedente P for falso (ou seja, se a pessoa não cumprir os requisitos), a premissa 2 NÃO existe.")
    out.append("Portanto, a regra não dispara, nenhuma conclusão positiva pode ser derivada, e o acesso NÃO é concedido.")
    out.append("Essa distinção é o que separa a mera sintaxe da implicação lógica do seu real significado semântico em sistemas baseados em conhecimento.")
    out.append("=" * 95)
    return "\n".join(out)

if __name__ == "__main__":
    print(format_truth_table_text())
