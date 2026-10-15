"""
src/state_machine.py
====================
Implementação da Máquina de Estados Finitos (FSM) para o ciclo de vida
de uma solicitação de acesso no Projeto Atlas Access (Etapa 5).

Estados:
1. Aguardando (Estado Inicial)
2. Em análise
3. Autorizada
4. Não autorizada (Estado Terminal)
5. Acesso em andamento
6. Acesso encerrado (Estado Terminal)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from datetime import datetime

class AccessState(str, Enum):
    AGUARDANDO = "Aguardando"
    EM_ANALISE = "Em análise"
    AUTORIZADA = "Autorizada"
    NAO_AUTORIZADA = "Não autorizada"
    ACESSO_EM_ANDAMENTO = "Acesso em andamento"
    ACESSO_ENCERRADO = "Acesso encerrado"

@dataclass
class TransitionLog:
    timestamp: str
    from_state: AccessState
    to_state: AccessState
    event_or_condition: str
    action: str
    justification: Optional[str] = None

class AccessRequestStateMachine:
    """
    Controla o ciclo de vida de uma solicitação de acesso para uma pessoa e uma área.
    """
    def __init__(self, requester: str, target_area: str):
        self.requester = requester
        self.target_area = target_area
        self.current_state: AccessState = AccessState.AGUARDANDO
        self.history: List[TransitionLog] = []

    def _log_transition(self, to_state: AccessState, event_or_condition: str, action: str, justification: Optional[str] = None):
        log = TransitionLog(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            from_state=self.current_state,
            to_state=to_state,
            event_or_condition=event_or_condition,
            action=action,
            justification=justification
        )
        self.history.append(log)
        self.current_state = to_state

    def receive_request(self) -> bool:
        if self.current_state == AccessState.AGUARDANDO:
            self._log_transition(
                to_state=AccessState.EM_ANALISE,
                event_or_condition="Solicitação de acesso recebida no terminal",
                action="Submeter consulta de conformidade ao motor de inferência Prolog"
            )
            return True
        return False

    def evaluate_result(self, proved_in_kb: bool, justification: str) -> AccessState:
        if self.current_state != AccessState.EM_ANALISE:
            raise ValueError(f"Não é possível avaliar a partir do estado '{self.current_state}'.")

        if proved_in_kb:
            self._log_transition(
                to_state=AccessState.AUTORIZADA,
                event_or_condition="Avaliação lógica concluída COM PROVA no SBC",
                action="Liberar acionamento da catraca/porta e gerar permissão temporária",
                justification=justification
            )
        else:
            self._log_transition(
                to_state=AccessState.NAO_AUTORIZADA,
                event_or_condition="Avaliação lógica concluída SEM PROVA no SBC (CWA)",
                action="Manter bloqueio físico e emitir relatório de justificativa ao solicitante",
                justification=justification
            )
        return self.current_state

    def confirm_entry(self) -> bool:
        if self.current_state == AccessState.AUTORIZADA:
            self._log_transition(
                to_state=AccessState.ACESSO_EM_ANDAMENTO,
                event_or_condition="Passagem confirmada pelos sensores da catraca/porta",
                action="Registrar timestamp de entrada no log de segurança e monitorar permanência"
            )
            return True
        return False

    def confirm_exit(self) -> bool:
        if self.current_state == AccessState.ACESSO_EM_ANDAMENTO:
            self._log_transition(
                to_state=AccessState.ACESSO_ENCERRADO,
                event_or_condition="Passagem de saída confirmada pelos sensores de saída",
                action="Registrar timestamp de saída e encerrar o ciclo da solicitação"
            )
            return True
        return False

    def get_summary(self) -> str:
        lines = [
            f"Solicitante: {self.requester} | Área Alvo: {self.target_area}",
            f"Estado Atual: {self.current_state.value}",
            "Histórico de Transições:"
        ]
        for idx, h in enumerate(self.history, 1):
            lines.append(f"  {idx}. [{h.from_state.value}] -> [{h.to_state.value}]")
            lines.append(f"     Evento/Condição: {h.event_or_condition}")
            lines.append(f"     Ação Realizada:  {h.action}")
            if h.justification:
                lines.append(f"     Justificativa:   {h.justification}")
        return "\n".join(lines)


def get_transition_table_data() -> List[Dict[str, str]]:
    """
    Retorna a tabela de transição oficial exigida na Etapa 5.
    """
    return [
        {
            "estado_atual": "Aguardando",
            "evento_condicao": "Solicitação recebida no terminal",
            "proximo_estado": "Em análise",
            "acao_justificativa": "Iniciar avaliação da solicitação e consultar o motor de inferência."
        },
        {
            "estado_atual": "Em análise",
            "evento_condicao": "Avaliação concluída com prova lógica na base (True)",
            "proximo_estado": "Autorizada",
            "acao_justificativa": "Sinalizar liberação física e destravar catraca/porta."
        },
        {
            "estado_atual": "Em análise",
            "evento_condicao": "Avaliação concluída sem prova lógica na base (False / CWA)",
            "proximo_estado": "Não autorizada",
            "acao_justificativa": "Manter bloqueio físico e fornecer a trilha de explicação."
        },
        {
            "estado_atual": "Autorizada",
            "evento_condicao": "Entrada confirmada (sensor da catraca acionado)",
            "proximo_estado": "Acesso em andamento",
            "acao_justificativa": "Registrar entrada e monitorar presença do indivíduo no setor."
        },
        {
            "estado_atual": "Acesso em andamento",
            "evento_condicao": "Saída confirmada (sensor de saída acionado)",
            "proximo_estado": "Acesso encerrado",
            "acao_justificativa": "Registrar saída no registro de segurança e fechar sessão."
        }
    ]
