"""
engine/prolog_interpreter.py
============================
Interpretador Prolog minimalista e formal em Python puro baseado em
Cláusulas de Horn e Resolução SLD (Selective Linear Definite).

Implementa:
- Leitura e parsing de arquivos Prolog (.pl) com fatos e regras.
- Unificação sintática formal (constante/constante, variável/termo, estruturas).
- Busca em profundidade:
    * Ordem de cláusulas: de cima para baixo no arquivo.
    * Ordem de objetivos: da esquerda para a direita no corpo da regra.
- Backtracking cronológico na falha.
- Rastreamento completo das 4 portas do Modelo de Caixa de Byrd (Call, Exit, Fail, Redo).
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
import re

# ------------------------------------------------------------------------------
# Representação dos Termos Prolog
# ------------------------------------------------------------------------------

class Term:
    pass

@dataclass(frozen=True)
class Atom(Term):
    name: str

    def __repr__(self):
        return self.name

@dataclass(frozen=True)
class Variable(Term):
    name: str

    def __repr__(self):
        return self.name

@dataclass(frozen=True)
class Compound(Term):
    functor: str
    args: Tuple[Term, ...]

    def __repr__(self):
        args_str = ", ".join(repr(arg) for arg in self.args)
        return f"{self.functor}({args_str})"

@dataclass
class Clause:
    head: Compound
    body: List[Compound]

    def __repr__(self):
        if not self.body:
            return f"{self.head}."
        body_str = ", ".join(repr(b) for b in self.body)
        return f"{self.head} :- {body_str}."

@dataclass
class TraceEvent:
    port: str       # 'Call', 'Exit', 'Fail', 'Redo'
    goal: Term
    depth: int
    rule_info: Optional[str] = None
    bindings: Optional[Dict[str, str]] = None

    def __repr__(self):
        indent = "  " * self.depth
        info = f" [{self.rule_info}]" if self.rule_info else ""
        return f"{indent}{self.port}: {self.goal}{info}"


# ------------------------------------------------------------------------------
# Algoritmo de Unificação
# ------------------------------------------------------------------------------

def is_variable(term: Term) -> bool:
    return isinstance(term, Variable)

def substitute(term: Term, subst: Dict[str, Term]) -> Term:
    if isinstance(term, Variable):
        if term.name in subst:
            return substitute(subst[term.name], subst)
        return term
    elif isinstance(term, Compound):
        return Compound(term.functor, tuple(substitute(arg, subst) for arg in term.args))
    return term

def unify(term1: Term, term2: Term, subst: Dict[str, Term]) -> Optional[Dict[str, Term]]:
    """
    Unificação formal seguindo as 3 regras:
    1. Constante com constante: iguais unificam.
    2. Variável livre com termo: liga a variável ao termo.
    3. Estruturas com estruturas: mesmo functor, mesma aridade e argumentos unificáveis.
    """
    t1 = substitute(term1, subst)
    t2 = substitute(term2, subst)

    if t1 == t2:
        return subst

    if is_variable(t1):
        new_subst = dict(subst)
        new_subst[t1.name] = t2
        return new_subst

    if is_variable(t2):
        new_subst = dict(subst)
        new_subst[t2.name] = t1
        return new_subst

    if isinstance(t1, Compound) and isinstance(t2, Compound):
        if t1.functor != t2.functor or len(t1.args) != len(t2.args):
            return None
        current_subst = dict(subst)
        for a1, a2 in zip(t1.args, t2.args):
            res = unify(a1, a2, current_subst)
            if res is None:
                return None
            current_subst = res
        return current_subst

    return None


# ------------------------------------------------------------------------------
# Parser de Sintaxe Prolog
# ------------------------------------------------------------------------------

class PrologParser:
    @staticmethod
    def parse_term(text: str) -> Term:
        text = text.strip()
        if not text:
            raise ValueError("Termo vazio")

        # Verifica se é átomo ou variável simples
        if "(" not in text:
            if text[0].isupper() or text.startswith("_"):
                return Variable(text)
            return Atom(text)

        # Estrutura composta
        m = re.match(r"^([a-z_][a-zA-Z0-9_]*)\((.*)\)$", text)
        if not m:
            raise ValueError(f"Sintaxe inválida para termo: {text}")
        functor = m.group(1)
        args_text = m.group(2)

        # Divisão dos argumentos respeitando parênteses aninhados
        args = []
        depth = 0
        current = []
        for char in args_text:
            if char == "," and depth == 0:
                args.append("".join(current).strip())
                current = []
            else:
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                current.append(char)
        if current:
            args.append("".join(current).strip())

        parsed_args = tuple(PrologParser.parse_term(a) for a in args)
        return Compound(functor, parsed_args)

    @staticmethod
    def parse_file(filepath: str) -> List[Clause]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove comentários de linha (% ...)
        lines = []
        for line in content.splitlines():
            line_clean = re.sub(r"%.*$", "", line).strip()
            if line_clean:
                lines.append(line_clean)
        full_text = " ".join(lines)

        clauses = []
        # Divide por '.' que encerram cláusulas
        raw_clauses = [c.strip() for c in full_text.split(".") if c.strip()]
        for raw in raw_clauses:
            if raw.startswith(":-"):
                # Diretivas (ex: :- consult(...)), ignora na base
                continue
            if ":-" in raw:
                head_part, body_part = raw.split(":-", 1)
                head_term = PrologParser.parse_term(head_part.strip())
                if not isinstance(head_term, Compound):
                    head_term = Compound(head_term.name, ())

                # Parse dos objetivos do corpo
                body_goals = []
                depth = 0
                current = []
                for char in body_part:
                    if char == "," and depth == 0:
                        body_goals.append("".join(current).strip())
                        current = []
                    else:
                        if char == "(":
                            depth += 1
                        elif char == ")":
                            depth -= 1
                        current.append(char)
                if current:
                    body_goals.append("".join(current).strip())

                body_terms = []
                for bg in body_goals:
                    if not bg:
                        continue
                    bt = PrologParser.parse_term(bg)
                    if isinstance(bt, Atom):
                        bt = Compound(bt.name, ())
                    body_terms.append(bt)

                clauses.append(Clause(head_term, body_terms))
            else:
                head_term = PrologParser.parse_term(raw.strip())
                if isinstance(head_term, Atom):
                    head_term = Compound(head_term.name, ())
                clauses.append(Clause(head_term, []))
        return clauses


# ------------------------------------------------------------------------------
# Motor de Inferência Prolog com Rastreamento 4-Portas
# ------------------------------------------------------------------------------

class PrologEngine:
    def __init__(self, clauses: Optional[List[Clause]] = None):
        self.clauses: List[Clause] = clauses or []
        self.var_counter = 0

    def load_file(self, filepath: str):
        self.clauses = PrologParser.parse_file(filepath)

    def _rename_vars(self, term: Term, suffix: int) -> Term:
        if isinstance(term, Variable):
            return Variable(f"{term.name}_{suffix}")
        elif isinstance(term, Compound):
            return Compound(term.functor, tuple(self._rename_vars(a, suffix) for a in term.args))
        return term

    def query(self, query_str: str, trace: bool = False) -> Tuple[bool, List[Dict[str, str]], List[TraceEvent]]:
        """
        Executa uma consulta Prolog e retorna:
        - Sucesso (bool): True se houve pelo menos uma prova, False caso contrário.
        - Soluções (List[Dict]): Mapeamento de variáveis para os termos unificados.
        - Trilha de Trace (List[TraceEvent]): Eventos Call/Exit/Fail/Redo.
        """
        raw_query = query_str.strip().rstrip(".")
        if raw_query.startswith("?-"):
            raw_query = raw_query[2:].strip()

        term = PrologParser.parse_term(raw_query)
        if isinstance(term, Atom):
            term = Compound(term.name, ())

        self.var_counter = 0
        trace_events: List[TraceEvent] = []
        solutions: List[Dict[str, str]] = []

        def solve(goals: List[Compound], subst: Dict[str, Term], depth: int) -> bool:
            if not goals:
                # Todos os objetivos foram resolvidos com sucesso!
                final_subst = {k: str(substitute(v, subst)) for k, v in subst.items() if not "_" in k}
                solutions.append(final_subst)
                return True

            current_goal = goals[0]
            rest_goals = goals[1:]
            ground_goal = substitute(current_goal, subst)

            if trace:
                trace_events.append(TraceEvent(port="Call", goal=ground_goal, depth=depth))

            goal_succeeded_at_least_once = False

            # Ordem de busca: cláusulas de cima para baixo no arquivo
            for idx, clause in enumerate(self.clauses):
                self.var_counter += 1
                c_head = self._rename_vars(clause.head, self.var_counter)
                c_body = [self._rename_vars(b, self.var_counter) for b in clause.body]

                unified_subst = unify(ground_goal, c_head, subst)
                if unified_subst is not None:
                    rule_label = f"Cláusula #{idx+1} ({c_head.functor}/{len(c_head.args)})"
                    # Ordem de busca: objetivos da esquerda para a direita
                    new_goals = c_body + rest_goals
                    if solve(new_goals, unified_subst, depth + 1):
                        goal_succeeded_at_least_once = True
                        if trace:
                            trace_events.append(TraceEvent(
                                port="Exit",
                                goal=ground_goal,
                                depth=depth,
                                rule_info=rule_label
                            ))
                        return True
                    else:
                        if trace:
                            trace_events.append(TraceEvent(
                                port="Redo",
                                goal=ground_goal,
                                depth=depth,
                                rule_info="Tentando alternativa via backtracking"
                            ))

            if not goal_succeeded_at_least_once:
                if trace:
                    trace_events.append(TraceEvent(port="Fail", goal=ground_goal, depth=depth))
            return False

        has_solution = solve([term], {}, 1)
        return has_solution, solutions, trace_events

    def is_c07_active(self) -> bool:
        """Verifica se o caso C07 (Gustavo) está atualmente ativo na base."""
        for c in self.clauses:
            if c.head.args and len(c.head.args) >= 1 and str(c.head.args[0]) == "gustavo":
                return True
        return False

    def activate_c07(self) -> bool:
        """Ativa o caso C07 (adiciona Gustavo como funcionário com credencial e treinamento)."""
        if self.is_c07_active():
            return False
        
        gustavo_clauses = [
            Clause(Compound("pessoa", (Atom("gustavo"),)), []),
            Clause(Compound("funcionario", (Atom("gustavo"),)), []),
            Clause(Compound("credencial_valida", (Atom("gustavo"),)), []),
            Clause(Compound("treinamento_concluido", (Atom("gustavo"),)), []),
        ]
        # Insere após os fatos de cada predicado ou no início das cláusulas
        self.clauses.extend(gustavo_clauses)
        return True

    def deactivate_c07(self) -> bool:
        """Desativa o caso C07 (remove completamente Gustavo da base de conhecimento)."""
        if not self.is_c07_active():
            return False

        self.clauses = [
            c for c in self.clauses
            if not (c.head.args and len(c.head.args) >= 1 and str(c.head.args[0]) == "gustavo")
        ]
        return True

