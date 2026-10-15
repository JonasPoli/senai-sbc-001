"""
tests/test_suite.py
===================
Suíte completa de testes automatizados para o Projeto Atlas Access.
Testa:
1. Base Original: Casos obrigatórios C01 a C06.
2. Base Evoluída:
   - Etapa 10 Parte A: Alteração de fato (Bruno no laboratório).
   - Etapa 10 Parte B: Nova regra R07 (Diego no escritório).
   - Etapa 11: Novo caso C07 (Gustavo no laboratório e na produção).
3. Propriedades do Motor de Inferência (Unificação, Backtracking e Trace 4-Portas).
4. Máquina de Estados Finitos (Transições e Ações).
5. Tabela-Verdade da Regra R05.
"""

import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
for p in [PROJECT_ROOT, os.path.join(PROJECT_ROOT, "python")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from engine.prolog_interpreter import PrologEngine
from engine.explanation_facility import explain_decision, CASES_METADATA
from engine.truth_table import generate_r05_truth_table

try:
    from state_machine import AccessRequestStateMachine, AccessState
except ImportError:
    from src.state_machine import AccessRequestStateMachine, AccessState

def get_kb_path(filename):
    for candidate in [
        os.path.join(PROJECT_ROOT, "prolog", filename),
        os.path.join(PROJECT_ROOT, "src", filename),
        os.path.join("prolog", filename),
        os.path.join("src", filename)
    ]:
        if os.path.exists(candidate):
            return candidate
    return filename

class TestAtlasAccessOriginal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = PrologEngine()
        cls.engine.load_file(get_kb_path("atlas_access.pl"))

    def test_c01_ana_producao(self):
        """C01: Ana / Produção -> Deve autorizar (R05 satisfeito)"""
        proved, sols, trace = self.engine.query("acesso(ana, producao)", trace=True)
        self.assertTrue(proved)
        self.assertTrue(any(ev.port == "Exit" and "producao" in str(ev.goal) for ev in trace))

    def test_c02_bruno_laboratorio(self):
        """C02: Bruno / Laboratório -> Não demonstrado (falta treinamento em R03)"""
        proved, sols, trace = self.engine.query("acesso(bruno, laboratorio)", trace=True)
        self.assertFalse(proved)

    def test_c03_carla_laboratorio(self):
        """C03: Carla / Laboratório -> Deve autorizar (R04 satisfeito)"""
        proved, sols, trace = self.engine.query("acesso(carla, laboratorio)", trace=True)
        self.assertTrue(proved)

    def test_c04_diego_producao(self):
        """C04: Diego / Produção -> Não demonstrado (falta autorização especial em R06)"""
        proved, sols, trace = self.engine.query("acesso(diego, producao)", trace=True)
        self.assertFalse(proved)
        # Verifica se tentou R05 primeiro, falhou, e fez backtracking para R06
        has_redo = any(ev.port == "Redo" for ev in trace)
        self.assertTrue(has_redo, "Deveria ocorrer backtracking de R05 para R06")

    def test_c05_elisa_laboratorio(self):
        """C05: Elisa / Laboratório -> Não demonstrado (visitante sem regra para laboratório)"""
        proved, sols, trace = self.engine.query("acesso(elisa, laboratorio)", trace=True)
        self.assertFalse(proved)

    def test_c06_fernando_producao(self):
        """C06: Fernando / Produção -> Não demonstrado (falta credencial válida em R05)"""
        proved, sols, trace = self.engine.query("acesso(fernando, producao)", trace=True)
        self.assertFalse(proved)


class TestAtlasAccessEvolucao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = PrologEngine()
        cls.engine.load_file(get_kb_path("atlas_access_evolucao.pl"))

    def test_etapa10_parte_a_bruno(self):
        """Etapa 10 Parte A: Bruno com treinamento concluído agora acessa o laboratório"""
        proved, _, _ = self.engine.query("acesso(bruno, laboratorio)")
        self.assertTrue(proved, "Com treinamento concluído, Bruno deve acessar o laboratório via R03")

    def test_etapa10_parte_b_diego_escritorio(self):
        """Etapa 10 Parte B: Diego (prestador com credencial e treinamento) acessa o escritório via R07"""
        proved, _, _ = self.engine.query("acesso(diego, escritorio)")
        self.assertTrue(proved, "Com a nova política R07, Diego deve acessar o escritório")

    def test_etapa11_c07_gustavo(self):
        """Etapa 11 C07: Gustavo acessa laboratório (R03), mas NÃO produção (falta S em R05)"""
        proved_lab, _, _ = self.engine.query("acesso(gustavo, laboratorio)")
        proved_prod, _, _ = self.engine.query("acesso(gustavo, producao)")
        self.assertTrue(proved_lab, "Gustavo deve acessar o laboratório via R03")
        self.assertFalse(proved_prod, "Gustavo NÃO deve acessar a produção sem autorização especial")


class TestStateMachine(unittest.TestCase):
    def test_successful_request_flow(self):
        sm = AccessRequestStateMachine("ana", "producao")
        self.assertEqual(sm.current_state, AccessState.AGUARDANDO)

        sm.receive_request()
        self.assertEqual(sm.current_state, AccessState.EM_ANALISE)

        sm.evaluate_result(proved_in_kb=True, justification="Cumpre R05")
        self.assertEqual(sm.current_state, AccessState.AUTORIZADA)

        sm.confirm_entry()
        self.assertEqual(sm.current_state, AccessState.ACESSO_EM_ANDAMENTO)

        sm.confirm_exit()
        self.assertEqual(sm.current_state, AccessState.ACESSO_ENCERRADO)

    def test_rejected_request_flow(self):
        sm = AccessRequestStateMachine("diego", "producao")
        sm.receive_request()
        sm.evaluate_result(proved_in_kb=False, justification="Falta autorização especial")
        self.assertEqual(sm.current_state, AccessState.NAO_AUTORIZADA)


class TestTruthTable(unittest.TestCase):
    def test_r05_table_counts(self):
        rows = generate_r05_truth_table()
        self.assertEqual(len(rows), 32)
        h_true = sum(1 for r in rows if r['H'] == 1)
        impl_true = sum(1 for r in rows if r['impl'] == 1)
        impl_false = sum(1 for r in rows if r['impl'] == 0)

        self.assertEqual(h_true, 2)
        self.assertEqual(impl_true, 31)
        self.assertEqual(impl_false, 1)


if __name__ == "__main__":
    unittest.main()
