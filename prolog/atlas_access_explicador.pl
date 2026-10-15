% ==============================================================================
% PROJETO ATLAS ACCESS - MOTOR DE EXPLICAÇÃO EM PROLOG (ETAPA 9)
% ==============================================================================
% Instituição: Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe, São Carlos/SP
% Equipe: Fábio, Fabi, Jonas Poli, Luciano
% ==============================================================================
% Arquivo: src/atlas_access_explicador.pl
% Descrição: Módulo de explicação e auditoria para gerar a trilha de justificativa
%            em linguagem natural, identificando os fatos sustentadores ou a
%            condição ausente que causou a falha de autorização.
% ==============================================================================

:- consult('atlas_access.pl').

% ------------------------------------------------------------------------------
% Predicado Principal: explicar_acesso/2
% Formato: explicar_acesso(+Pessoa, +Area).
% Imprime na tela o veredito, a regra aplicada ou analisada, e a justificativa
% detalhada em linguagem natural.
% ------------------------------------------------------------------------------
explicar_acesso(Pessoa, Area) :-
    acesso(Pessoa, Area),
    !,
    format('~n==================================================================~n', []),
    format('SOLICITAÇÃO: ~w -> Área ~w~n', [Pessoa, Area]),
    format('RESULTADO:   AUTORIZADO (True)~n', []),
    format('ESTADO FSM:  Em análise -> Autorizada~n', []),
    detalhar_sucesso(Pessoa, Area),
    format('==================================================================~n', []).

explicar_acesso(Pessoa, Area) :-
    format('~n==================================================================~n', []),
    format('SOLICITAÇÃO: ~w -> Área ~w~n', [Pessoa, Area]),
    format('RESULTADO:   NÃO AUTORIZADO (Não demonstrado na base / False)~n', []),
    format('ESTADO FSM:  Em análise -> Não autorizada~n', []),
    detalhar_falha(Pessoa, Area),
    format('==================================================================~n', []).

% ------------------------------------------------------------------------------
% Detalhamento dos Casos de Sucesso
% ------------------------------------------------------------------------------
detalhar_sucesso(Pessoa, recepcao) :-
    format('REGRA:       R01 (U -> AR)~n', []),
    format('FATOS:       pessoa(~w) presente na base.~n', [Pessoa]),
    format('JUSTIFICATIVA: Acesso autorizado porque a Recepção é área de livre atendimento para qualquer pessoa cadastrada.~n', []).

detalhar_sucesso(Pessoa, escritorio) :-
    funcionario(Pessoa),
    credencial_valida(Pessoa),
    format('REGRA:       R02 ((F ∧ C) -> AE)~n', []),
    format('FATOS:       funcionario(~w), credencial_valida(~w).~n', [Pessoa, Pessoa]),
    format('JUSTIFICATIVA: Acesso autorizado porque ~w é funcionário(a) e possui credencial válida, conforme a regra R02.~n', [Pessoa]).

detalhar_sucesso(Pessoa, laboratorio) :-
    funcionario(Pessoa),
    credencial_valida(Pessoa),
    treinamento_concluido(Pessoa),
    format('REGRA:       R03 ((F ∧ C ∧ T) -> AL)~n', []),
    format('FATOS:       funcionario(~w), credencial_valida(~w), treinamento_concluido(~w).~n', [Pessoa, Pessoa, Pessoa]),
    format('JUSTIFICATIVA: Acesso autorizado porque ~w é funcionário(a), possui credencial válida e concluiu o treinamento, conforme a regra R03.~n', [Pessoa]).

detalhar_sucesso(Pessoa, laboratorio) :-
    prestador(Pessoa),
    credencial_valida(Pessoa),
    treinamento_concluido(Pessoa),
    autorizacao_especial(Pessoa),
    format('REGRA:       R04 ((P ∧ C ∧ T ∧ S) -> AL)~n', []),
    format('FATOS:       prestador(~w), credencial_valida(~w), treinamento_concluido(~w), autorizacao_especial(~w).~n', [Pessoa, Pessoa, Pessoa, Pessoa]),
    format('JUSTIFICATIVA: Acesso autorizado porque ~w é prestador(a), possui credencial válida, concluiu treinamento e possui autorização especial da Segurança do Trabalho, conforme a regra R04.~n', [Pessoa]).

detalhar_sucesso(Pessoa, producao) :-
    funcionario(Pessoa),
    credencial_valida(Pessoa),
    treinamento_concluido(Pessoa),
    autorizacao_especial(Pessoa),
    format('REGRA:       R05 ((F ∧ C ∧ T ∧ S) -> AP)~n', []),
    format('FATOS:       funcionario(~w), credencial_valida(~w), treinamento_concluido(~w), autorizacao_especial(~w).~n', [Pessoa, Pessoa, Pessoa, Pessoa]),
    format('JUSTIFICATIVA: Acesso autorizado porque ~w é funcionário(a) e cumpre todos os requisitos mais rigorosos: credencial válida, treinamento e autorização especial, conforme a regra R05.~n', [Pessoa]).

detalhar_sucesso(Pessoa, producao) :-
    prestador(Pessoa),
    credencial_valida(Pessoa),
    treinamento_concluido(Pessoa),
    autorizacao_especial(Pessoa),
    format('REGRA:       R06 ((P ∧ C ∧ T ∧ S) -> AP)~n', []),
    format('FATOS:       prestador(~w), credencial_valida(~w), treinamento_concluido(~w), autorizacao_especial(~w).~n', [Pessoa, Pessoa, Pessoa, Pessoa]),
    format('JUSTIFICATIVA: Acesso autorizado porque ~w é prestador(a) e cumpre todos os requisitos da Área de Produção: credencial válida, treinamento e autorização especial, conforme a regra R06.~n', [Pessoa]).

% ------------------------------------------------------------------------------
% Detalhamento dos Casos de Falha (Diagnóstico Semântico e CWA)
% ------------------------------------------------------------------------------
detalhar_falha(Pessoa, Area) :-
    visitante(Pessoa),
    Area \= recepcao,
    !,
    format('REGRA:       NENHUMA REGRA APLICÁVEL NA BASE~n', []),
    format('FATOS:       visitante(~w).~n', [Pessoa]),
    format('DIAGNÓSTICO: Elisa é visitante. A IT-SEG-014 estipula que visitantes permanecem na Recepção durante toda a estadia.~n', []),
    format('JUSTIFICATIVA: Não foi possível autorizar porque visitantes não possuem permissão de acesso a áreas controladas ou administrativas.~n', []).

detalhar_falha(Pessoa, escritorio) :-
    \+ funcionario(Pessoa),
    !,
    format('REGRA:       R02 ((F ∧ C) -> AE)~n', []),
    format('COND. FALHA: Falta vínculo de funcionário (~w não é funcionário registrado).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque o Escritório Administrativo é restrito ao pessoal próprio (funcionários).~n', []).

detalhar_falha(Pessoa, escritorio) :-
    funcionario(Pessoa),
    \+ credencial_valida(Pessoa),
    !,
    format('REGRA:       R02 ((F ∧ C) -> AE)~n', []),
    format('COND. FALHA: Falta credencial_valida(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque ~w é funcionário(a), mas não possui credencial válida cadastrada.~n', [Pessoa]).

detalhar_falha(Pessoa, laboratorio) :-
    funcionario(Pessoa),
    !,
    format('REGRA:       R03 ((F ∧ C ∧ T) -> AL)~n', []),
    diagnosticar_condicoes_laboratorio_func(Pessoa).

detalhar_falha(Pessoa, laboratorio) :-
    prestador(Pessoa),
    !,
    format('REGRA:       R04 ((P ∧ C ∧ T ∧ S) -> AL)~n', []),
    diagnosticar_condicoes_laboratorio_prest(Pessoa).

detalhar_falha(Pessoa, producao) :-
    funcionario(Pessoa),
    !,
    format('REGRA:       R05 ((F ∧ C ∧ T ∧ S) -> AP)~n', []),
    diagnosticar_condicoes_producao(Pessoa).

detalhar_falha(Pessoa, producao) :-
    prestador(Pessoa),
    !,
    format('REGRA:       R06 ((P ∧ C ∧ T ∧ S) -> AP)~n', []),
    diagnosticar_condicoes_producao(Pessoa).

% Diagnósticos específicos de condições ausentes
diagnosticar_condicoes_laboratorio_func(Pessoa) :-
    \+ credencial_valida(Pessoa),
    !,
    format('COND. FALHA: Falta credencial_valida(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque a credencial não está válida (crachá vencido ou inexistente).~n', []).

diagnosticar_condicoes_laboratorio_func(Pessoa) :-
    \+ treinamento_concluido(Pessoa),
    !,
    format('COND. FALHA: Falta treinamento_concluido(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque o funcionário não concluiu o treinamento obrigatório para o Laboratório (Regra R03).~n', []).

diagnosticar_condicoes_laboratorio_prest(Pessoa) :-
    \+ credencial_valida(Pessoa),
    !,
    format('COND. FALHA: Falta credencial_valida(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque prestadores necessitam de credencial válida.~n', []).

diagnosticar_condicoes_laboratorio_prest(Pessoa) :-
    \+ treinamento_concluido(Pessoa),
    !,
    format('COND. FALHA: Falta treinamento_concluido(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque o prestador não possui treinamento concluído.~n', []).

diagnosticar_condicoes_laboratorio_prest(Pessoa) :-
    \+ autorizacao_especial(Pessoa),
    !,
    format('COND. FALHA: Falta autorizacao_especial(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque falta a autorização especial emitida pela Segurança do Trabalho exigida para prestadores no Laboratório (Regra R04).~n', []).

diagnosticar_condicoes_producao(Pessoa) :-
    \+ credencial_valida(Pessoa),
    !,
    format('COND. FALHA: Falta credencial_valida(~w) (Crachá vencido ou inválido).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque ninguém entra em área controlada sem credencial válida; crachá vencido não entra de jeito nenhum.~n', []).

diagnosticar_condicoes_producao(Pessoa) :-
    \+ treinamento_concluido(Pessoa),
    !,
    format('COND. FALHA: Falta treinamento_concluido(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque a Área de Produção exige treinamento concluído.~n', []).

diagnosticar_condicoes_producao(Pessoa) :-
    \+ autorizacao_especial(Pessoa),
    !,
    format('COND. FALHA: Falta autorizacao_especial(~w).~n', [Pessoa]),
    format('JUSTIFICATIVA: Não foi possível autorizar porque falta a autorização especial emitida pela Segurança do Trabalho exigida na Produção.~n', []).

% ------------------------------------------------------------------------------
% Auditoria de todos os Casos Obrigatórios (C01 a C06)
% ------------------------------------------------------------------------------
auditar_todos :-
    format('~n==================================================================~n', []),
    format('AUDITORIA COMPLETA DOS SEIS CASOS OBRIGATÓRIOS (C01 A C06)~n', []),
    format('==================================================================~n', []),
    explicar_acesso(ana, producao),
    explicar_acesso(bruno, laboratorio),
    explicar_acesso(carla, laboratorio),
    explicar_acesso(diego, producao),
    explicar_acesso(elisa, laboratorio),
    explicar_acesso(fernando, producao).
