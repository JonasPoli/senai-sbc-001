"""
engine/explanation_facility.py
==============================
Módulo de Explicação (Explanation Facility) para o Projeto Atlas Access.
Produz a trilha de justificativa em linguagem natural e a Matriz de Validação
Cruzada de rastreabilidade (Etapa 9).
"""

from typing import Dict, Any, List, Optional
from engine.prolog_interpreter import PrologEngine

CASES_METADATA = [
    {
        "id": "C01",
        "pessoa": "ana",
        "area": "producao",
        "categoria": "funcionario",
        "regra_id": "R05",
        "expressao_logica": "(F ∧ C ∧ T ∧ S) -> AP",
        "consulta": "acesso(ana, producao)",
        "resultado_esperado": True,
        "fatos_sustentam": "funcionario(ana), credencial_valida(ana), treinamento_concluido(ana), autorizacao_especial(ana)",
        "condicao_decisiva": "Todas as 4 condições satisfeitas",
        "justificativa": "Acesso autorizado à Área de Produção para Ana: funcionária com credencial válida, treinamento concluído e autorização especial emitida pela Segurança do Trabalho, atendendo integralmente à regra R05.",
        "estado_esperado": "Autorizada"
    },
    {
        "id": "C02",
        "pessoa": "bruno",
        "area": "laboratorio",
        "categoria": "funcionario",
        "regra_id": "R03",
        "expressao_logica": "(F ∧ C ∧ T) -> AL",
        "consulta": "acesso(bruno, laboratorio)",
        "resultado_esperado": False,
        "fatos_sustentam": "funcionario(bruno), credencial_valida(bruno)",
        "condicao_decisiva": "Falta treinamento_concluido(bruno) (T = 0)",
        "justificativa": "Acesso não autorizado ao Laboratório Técnico para Bruno: embora seja funcionário com credencial válida, não possui treinamento concluído exigido pela regra R03.",
        "estado_esperado": "Não autorizada"
    },
    {
        "id": "C03",
        "pessoa": "carla",
        "area": "laboratorio",
        "categoria": "prestador",
        "regra_id": "R04",
        "expressao_logica": "(P ∧ C ∧ T ∧ S) -> AL",
        "consulta": "acesso(carla, laboratorio)",
        "resultado_esperado": True,
        "fatos_sustentam": "prestador(carla), credencial_valida(carla), treinamento_concluido(carla), autorizacao_especial(carla)",
        "condicao_decisiva": "Todas as 4 condições satisfeitas para prestador",
        "justificativa": "Acesso autorizado ao Laboratório Técnico para Carla: prestadora de serviço com credencial válida, treinamento concluído e autorização especial da Segurança do Trabalho, conforme a regra R04.",
        "estado_esperado": "Autorizada"
    },
    {
        "id": "C04",
        "pessoa": "diego",
        "area": "producao",
        "categoria": "prestador",
        "regra_id": "R06",
        "expressao_logica": "(P ∧ C ∧ T ∧ S) -> AP",
        "consulta": "acesso(diego, producao)",
        "resultado_esperado": False,
        "fatos_sustentam": "prestador(diego), credencial_valida(diego), treinamento_concluido(diego)",
        "condicao_decisiva": "Falta autorizacao_especial(diego) (S = 0)",
        "justificativa": "Acesso não autorizado à Área de Produção para Diego: prestador de serviço com credencial e treinamento, porém sem autorização especial exigida para áreas de produção pela regra R06.",
        "estado_esperado": "Não autorizada"
    },
    {
        "id": "C05",
        "pessoa": "elisa",
        "area": "laboratorio",
        "categoria": "visitante",
        "regra_id": "Nenhuma aplicável",
        "expressao_logica": "Inexistente na base para visitante em área controlada",
        "consulta": "acesso(elisa, laboratorio)",
        "resultado_esperado": False,
        "fatos_sustentam": "visitante(elisa), credencial_valida(elisa)",
        "condicao_decisiva": "Ausência de regra autorizativa na base para a categoria Visitante fora da Recepção",
        "justificativa": "Acesso não autorizado ao Laboratório Técnico para Elisa: visitantes não possuem permissão de acesso a áreas controladas segundo a IT-SEG-014; inexiste regra aplicável na base de conhecimento.",
        "estado_esperado": "Não autorizada"
    },
    {
        "id": "C06",
        "pessoa": "fernando",
        "area": "producao",
        "categoria": "funcionario",
        "regra_id": "R05",
        "expressao_logica": "(F ∧ C ∧ T ∧ S) -> AP",
        "consulta": "acesso(fernando, producao)",
        "resultado_esperado": False,
        "fatos_sustentam": "funcionario(fernando), treinamento_concluido(fernando), autorizacao_especial(fernando)",
        "condicao_decisiva": "Falta credencial_valida(fernando) (C = 0 - crachá vencido)",
        "justificativa": "Acesso não autorizado à Área de Produção para Fernando: funcionário com treinamento e autorização especial, mas com crachá vencido / sem credencial válida cadastrada (regra R05 não satisfeita).",
        "estado_esperado": "Não autorizada"
    },
    {
        "id": "C07",
        "pessoa": "gustavo",
        "area": "laboratorio",
        "categoria": "funcionario",
        "regra_id": "R03",
        "expressao_logica": "(F ∧ C ∧ T) -> AL",
        "consulta": "acesso(gustavo, laboratorio)",
        "resultado_esperado": True,
        "fatos_sustentam": "funcionario(gustavo), credencial_valida(gustavo), treinamento_concluido(gustavo)",
        "condicao_decisiva": "Todas as 3 condições satisfeitas para laboratório",
        "justificativa": "Acesso autorizado ao Laboratório Técnico para Gustavo (Caso C07): funcionário com credencial válida e treinamento concluído, atendendo integralmente aos requisitos da regra R03.",
        "estado_esperado": "Autorizada"
    }
]

def explain_decision(pessoa: str, area: str, engine: PrologEngine) -> Dict[str, Any]:
    query_str = f"acesso({pessoa}, {area})"
    proved, sols, trace = engine.query(query_str, trace=True)

    # Verifica fatos conhecidos na base
    is_func, _, _ = engine.query(f"funcionario({pessoa})")
    is_prest, _, _ = engine.query(f"prestador({pessoa})")
    is_visit, _, _ = engine.query(f"visitante({pessoa})")
    has_cred, _, _ = engine.query(f"credencial_valida({pessoa})")
    has_train, _, _ = engine.query(f"treinamento_concluido({pessoa})")
    has_spec, _, _ = engine.query(f"autorizacao_especial({pessoa})")

    category = "funcionario" if is_func else ("prestador" if is_prest else ("visitante" if is_visit else "desconhecido"))

    if proved:
        if area == "recepcao":
            rule = "R01"
            formula = "U -> AR"
            facts = f"pessoa({pessoa})"
            just = f"Acesso autorizado à Recepção para {pessoa.capitalize()}: área de livre atendimento a qualquer pessoa cadastrada (Regra R01)."
        elif area == "escritorio":
            if is_func:
                rule = "R02"
                formula = "(F ∧ C) -> AE"
                facts = f"funcionario({pessoa}), credencial_valida({pessoa})"
                just = f"Acesso autorizado ao Escritório Administrativo para {pessoa.capitalize()}: funcionário com credencial válida (Regra R02)."
            else:
                rule = "R07"
                formula = "(P ∧ C ∧ T) -> AE"
                facts = f"prestador({pessoa}), credencial_valida({pessoa}), treinamento_concluido({pessoa})"
                just = f"Acesso autorizado ao Escritório Administrativo para {pessoa.capitalize()}: prestador com credencial e treinamento (Nova Política R07)."
        elif area == "laboratorio":
            if is_func:
                rule = "R03"
                formula = "(F ∧ C ∧ T) -> AL"
                facts = f"funcionario({pessoa}), credencial_valida({pessoa}), treinamento_concluido({pessoa})"
                just = f"Acesso autorizado ao Laboratório Técnico para {pessoa.capitalize()}: funcionário com credencial válida e treinamento concluído (Regra R03)."
            else:
                rule = "R04"
                formula = "(P ∧ C ∧ T ∧ S) -> AL"
                facts = f"prestador({pessoa}), credencial_valida({pessoa}), treinamento_concluido({pessoa}), autorizacao_especial({pessoa})"
                just = f"Acesso autorizado ao Laboratório Técnico para {pessoa.capitalize()}: prestador com credencial, treinamento e autorização especial (Regra R04)."
        else: # producao
            rule = "R05" if is_func else "R06"
            formula = f"({ 'F' if is_func else 'P' } ∧ C ∧ T ∧ S) -> AP"
            facts = f"{category}({pessoa}), credencial_valida({pessoa}), treinamento_concluido({pessoa}), autorizacao_especial({pessoa})"
            just = f"Acesso autorizado à Área de Produção para {pessoa.capitalize()}: {category} cumpre todos os requisitos (credencial, treinamento e autorização especial) conforme a regra {rule}."

        state = "Autorizada"
    else:
        state = "Não autorizada"
        if is_visit and area != "recepcao":
            rule = "Inexistente"
            formula = "Sem regra para visitantes fora da Recepção"
            facts = f"visitante({pessoa})"
            just = f"Não foi possível autorizar o acesso de {pessoa.capitalize()} à área '{area}': visitantes não possuem permissão de circulação fora da Recepção."
        elif area == "escritorio":
            rule = "R02"
            formula = "(F ∧ C) -> AE"
            missing = []
            if not is_func: missing.append("vínculo de funcionário")
            if not has_cred: missing.append("credencial válida")
            facts = f"{category}({pessoa})"
            just = f"Não foi possível autorizar o acesso ao Escritório Administrativo para {pessoa.capitalize()}: falta {', '.join(missing)}."
        elif area == "laboratorio":
            rule = "R03" if is_func else "R04"
            formula = "(F ∧ C ∧ T) -> AL" if is_func else "(P ∧ C ∧ T ∧ S) -> AL"
            missing = []
            if not has_cred: missing.append("credencial válida")
            if not has_train: missing.append("treinamento concluído")
            if is_prest and not has_spec: missing.append("autorização especial da Segurança do Trabalho")
            facts = f"{category}({pessoa})"
            just = f"Não foi possível autorizar o acesso ao Laboratório Técnico para {pessoa.capitalize()}: não consta na base {', '.join(missing)} (Regra {rule} não satisfeita)."
        else: # producao
            rule = "R05" if is_func else "R06"
            formula = f"({ 'F' if is_func else 'P' } ∧ C ∧ T ∧ S) -> AP"
            missing = []
            if not has_cred: missing.append("credencial válida (crachá vencido ou ausente)")
            if not has_train: missing.append("treinamento concluído")
            if not has_spec: missing.append("autorização especial")
            facts = f"{category}({pessoa})"
            just = f"Não foi possível autorizar o acesso à Área de Produção para {pessoa.capitalize()}: não consta na base {', '.join(missing)} exigida pela regra {rule}."

    return {
        "pessoa": pessoa,
        "area": area,
        "resultado": proved,
        "regra": rule,
        "formula": formula,
        "fatos": facts,
        "estado": state,
        "justificativa": just,
        "trace": trace
    }
