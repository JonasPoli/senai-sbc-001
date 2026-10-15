% ==============================================================================
% PROJETO ATLAS ACCESS - APRESENTAÇÃO DE 40 MINUTOS (SLIDES 10 AO 14)
% ==============================================================================
% Instituição: Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe, São Carlos/SP
% Curso: Pós-Graduação Lato Sensu em Inteligência Artificial
% Unidades Curriculares: Lógica para IA & Sistemas Baseados em Conhecimento (SBC)
% Bloco de Apresentação: Jonas Poli (Tempo: 18:00 às 27:00 - Total: 9 minutos)
% ==============================================================================
% Arquivo: src/apresentacao_jonas.pl (também acessível como slides_10_a_14.pl)
%
% COMO EXECUTAR NO TERMINAL (SWI-PROLOG):
%   $ swipl src/apresentacao_jonas.pl
%
% COMANDOS DISPONÍVEIS NO REPL:
%   ?- slide10.          % Slide 10: Fatos, regras e inferência (Ana)
%   ?- slide11.          % Slide 11: Regra Prolog e unificação
%   ?- slide12.          % Slide 12: Ana - Prova bem-sucedida (Trace)
%   ?- slide13.          % Slide 13: Diego - Alternativas e falha (Backtracking)
%   ?- slide14.          % Slide 14: Previsão e execução dos 6 casos
%   ?- apresentar_tudo.  % Apresentação completa dos Slides 10 ao 14
%   ?- ativar_c07.       % Etapa 11: Ativa o caso C07 (Gustavo)
%   ?- desativar_c07.    % Etapa 11: Desativa o caso C07 (remove Gustavo)
%   ?- status_c07.       % Verifica se C07 está ativo ou inativo
% ==============================================================================

% ==============================================================================
% DIRETIVAS DINÂMICAS (Permite assertz/retractall dinâmicos em tempo de execução)
% ==============================================================================
:- dynamic pessoa/1.
:- dynamic funcionario/1.
:- dynamic prestador/1.
:- dynamic visitante/1.
:- dynamic credencial_valida/1.
:- dynamic treinamento_concluido/1.
:- dynamic autorizacao_especial/1.

% ==============================================================================
% BASE DE CONHECIMENTO COMPLETA (Fatos Positivos e Regras R01 a R06)
% ==============================================================================

% --- Fatos Declarados: Pessoas ---
pessoa(ana).
pessoa(bruno).
pessoa(carla).
pessoa(diego).
pessoa(elisa).
pessoa(fernando).

% --- Fatos Declarados: Categorias ---
funcionario(ana).
funcionario(bruno).
funcionario(fernando).

prestador(carla).
prestador(diego).

visitante(elisa).

% --- Fatos Declarados: Condição C (Credencial Válida) ---
% Fernando tem crachá vencido / credencial inválida, portanto NÃO consta.
credencial_valida(ana).
credencial_valida(bruno).
credencial_valida(carla).
credencial_valida(diego).
credencial_valida(elisa).

% --- Fatos Declarados: Condição T (Treinamento Concluído) ---
% Bruno e Elisa não concluíram treinamento, portanto NÃO constam.
treinamento_concluido(ana).
treinamento_concluido(carla).
treinamento_concluido(diego).
treinamento_concluido(fernando).

% --- Fatos Declarados: Condição S (Autorização Especial da Seg. do Trabalho) ---
% Bruno, Diego e Elisa não possuem autorização especial, portanto NÃO constam.
autorizacao_especial(ana).
autorizacao_especial(carla).
autorizacao_especial(fernando).


% ==============================================================================
% REGRAS OPERACIONAIS DE ACESSO (R01 a R06)
% ==============================================================================

% R01: Recepção (Livre atendimento a pessoas cadastradas)
acesso(X, recepcao) :-
    pessoa(X).

% R02: Escritório Administrativo para Funcionários
acesso(X, escritorio) :-
    funcionario(X),
    credencial_valida(X).

% R03: Laboratório Técnico para Funcionários
acesso(X, laboratorio) :-
    funcionario(X),
    credencial_valida(X),
    treinamento_concluido(X).

% R04: Laboratório Técnico para Prestadores
acesso(X, laboratorio) :-
    prestador(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).

% R05: Área de Produção para Funcionários
acesso(X, producao) :-
    funcionario(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).

% R06: Área de Produção para Prestadores
acesso(X, producao) :-
    prestador(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).


% ==============================================================================
% PREDICADOS DE DEMONSTRAÇÃO DOS SLIDES 10 A 14 (APRESENTAÇÃO JONAS)
% ==============================================================================

% ------------------------------------------------------------------------------
% SLIDE 10: Fatos, regras e inferência (18:00 - 19:00 | 1:00 min)
% ------------------------------------------------------------------------------
slide10 :-
    format('~n================================================================================~n', []),
    format('SLIDE 10: FATOS, REGRAS E INFERÊNCIA (Etapas 6 e 7 | 18:00-19:00)~n', []),
    format('Apresentador: Jonas~n', []),
    format('================================================================================~n', []),
    format('1. FATOS POSITIVOS DECLARADOS SOBRE ANA:~n', []),
    format('   funcionario(ana).~n', []),
    format('   credencial_valida(ana).~n', []),
    format('   treinamento_concluido(ana).~n', []),
    format('   autorizacao_especial(ana).~n~n', []),
    format('2. CONSULTA SUBMETIDA AO MOTOR DE INFERÊNCIA:~n', []),
    format('   ?- acesso(ana, producao).~n~n', []),
    format('3. CONCEITO CENTRAL:~n', []),
    format('   O conhecimento declarativo fica totalmente separado do motor de inferência.~n', []),
    format('   O Prolog não calcula um procedimento estático: ele busca ativamente uma PROVA~n', []),
    format('   dedutiva que sustente a pergunta a partir dos fatos e da regra R05.~n', []),
    format('4. RESULTADO DA EXECUÇÃO: ', []),
    ( acesso(ana, producao) ->
        format('TRUE (Acesso demonstrado com sucesso!)~n', [])
    ;
        format('FALSE (Inesperado)~n', [])
    ),
    format('================================================================================~n~n', []).


% ------------------------------------------------------------------------------
% SLIDE 11: Regra Prolog e unificação (19:00 - 21:00 | 2:00 min)
% ------------------------------------------------------------------------------
slide11 :-
    format('~n================================================================================~n', []),
    format('SLIDE 11: REGRA PROLOG E UNIFICAÇÃO (Etapas 6 e 7 | 19:00-21:00)~n', []),
    format('Apresentador: Jonas~n', []),
    format('================================================================================~n', []),
    format('1. ESTRUTURA DA REGRA R05 (Cláusula de Horn Definida):~n', []),
    format('   acesso(X, producao) :-~n', []),
    format('       funcionario(X),~n', []),
    format('       credencial_valida(X),~n', []),
    format('       treinamento_concluido(X),~n', []),
    format('       autorizacao_especial(X).~n~n', []),
    format('2. AS TRÊS REGRAS FORMAIS DE UNIFICAÇÃO NO PROLOG:~n', []),
    format('   +-------------------------+------------------------------------------------+~n', []),
    format('   | Regra de Unificação     | Exemplo Aplicado neste Caso                    |~n', []),
    format('   +-------------------------+------------------------------------------------+~n', []),
    format('   | 1. Constantes iguais    | O átomo "producao" unifica com "producao".     |~n', []),
    format('   | 2. Variável livre/termo | A variável livre "X" unifica e instancia "ana".|~n', []),
    format('   | 3. Estruturas compatív. | Mesmo predicado, mesma aridade e argumentos    |~n', []),
    format('   |                         | unificáveis: acesso/2 unifica com acesso/2.    |~n', []),
    format('   +-------------------------+------------------------------------------------+~n~n', []),
    format('3. ORDEM DE EXECUÇÃO DETERMINÍSTICA DO MOTOR:~n', []),
    format('   - Cláusulas examinadas de CIMA PARA BAIXO no arquivo.~n', []),
    format('   - Objetivos do corpo tentados da ESQUERDA PARA A DIREITA.~n', []),
    format('================================================================================~n~n', []).


% ------------------------------------------------------------------------------
% SLIDE 12: Ana: uma prova bem-sucedida (21:00 - 22:30 | 1:30 min)
% ------------------------------------------------------------------------------
slide12 :-
    format('~n================================================================================~n', []),
    format('SLIDE 12: ANA - UMA PROVA BEM-SUCEDIDA (Etapas 7 e 8 | 21:00-22:30)~n', []),
    format('Apresentador: Jonas~n', []),
    format('================================================================================~n', []),
    format('Consulta: ?- acesso(ana, producao).~n~n', []),
    format('LEITURA DO TRACE PELO MODELO DE CAIXA DE 4 PORTAS (BYRD BOX MODEL):~n', []),
    format('  Passo 1:  Call: acesso(ana, producao)~n', []),
    format('            Motor busca cláusula com cabeça unificável: unifica com R05 (X = ana).~n', []),
    format('  Passo 2:    Call: funcionario(ana)~n', []),
    format('              Exit: funcionario(ana)       [Fato presente na base]~n', []),
    format('  Passo 3:    Call: credencial_valida(ana)~n', []),
    format('              Exit: credencial_valida(ana) [Fato presente na base]~n', []),
    format('  Passo 4:    Call: treinamento_concluido(ana)~n', []),
    format('              Exit: treinamento_concluido(ana) [Fato presente na base]~n', []),
    format('  Passo 5:    Call: autorizacao_especial(ana)~n', []),
    format('              Exit: autorizacao_especial(ana)  [Fato presente na base]~n', []),
    format('  Passo 6:  Exit: acesso(ana, producao)~n', []),
    format('Resultado: true~n~n', []),
    format('CONHECIMENTO USADO: Todos os 4 objetivos do corpo de R05 tiveram sucesso~n', []),
    format('com X = ana. Não houve falha, portanto NÃO ocorreu backtracking.~n', []),
    format('DICA DE APRESENTAÇÃO: No SWI-Prolog real, você pode digitar:~n', []),
    format('   ?- trace, acesso(ana, producao), notrace.~n', []),
    format('================================================================================~n~n', []).


% ------------------------------------------------------------------------------
% SLIDE 13: Diego: alternativas e falha (22:30 - 25:00 | 2:30 min)
% ------------------------------------------------------------------------------
slide13 :-
    format('~n================================================================================~n', []),
    format('SLIDE 13: DIEGO - ALTERNATIVAS E FALHA (Etapas 7 e 8 | 22:30-25:00)~n', []),
    format('Apresentador: Jonas~n', []),
    format('================================================================================~n', []),
    format('Consulta: ?- acesso(diego, producao).~n~n', []),
    format('RASTREAMENTO PASSO A PASSO (BACKTRACKING E AS 4 PORTAS):~n', []),
    format('  +-------+--------------------------------------+---------------+----------------------------+~n', []),
    format('  | Passo | Objetivo / Alternativa Tentada       | Porta Byrd    | Observação / Diagnóstico   |~n', []),
    format('  +-------+--------------------------------------+---------------+----------------------------+~n', []),
    format('  | 1     | funcionario(diego) [em R05]          | Call -> FAIL  | Diego não é funcionário    |~n', []),
    format('  | 2     | acesso(diego, producao)              | REDO          | Backtracking busca altern. |~n', []),
    format('  |       | Alternativa encontrada: Regra R06    |               | Cláusula seguinte no arq.  |~n', []),
    format('  | 3     | prestador(diego)                     | Call -> EXIT  | Fato confirmado na base    |~n', []),
    format('  | 4     | credencial_valida(diego)             | Call -> EXIT  | Fato confirmado na base    |~n', []),
    format('  | 5     | treinamento_concluido(diego)         | Call -> EXIT  | Fato confirmado na base    |~n', []),
    format('  | 6     | autorizacao_especial(diego)          | Call -> FAIL  | CONDIÇÃO AUSENTE NA BASE!  |~n', []),
    format('  | 7     | acesso(diego, producao)              | FAIL          | Sem mais regras no arquivo |~n', []),
    format('  +-------+--------------------------------------+---------------+----------------------------+~n', []),
    format('Resultado: false~n~n', []),
    format('PONTO CRÍTICO PARA A BANCA EXAMINADORA:~n', []),
    format('  - O backtracking esgotou o espaço de possibilidades ordenado.~n', []),
    format('  - O resultado FALSE não prova que Diego está proibido para sempre no mundo real;~n', []),
    format('    ele expressa estritamente a PRESUNÇÃO DE MUNDO FECHADO (CWA):~n', []),
    format('    "Com a base de fatos e regras atualmente disponível, a autorização não é derivável".~n', []),
    format('================================================================================~n~n', []).


% ------------------------------------------------------------------------------
% SLIDE 14: Previsão e execução (25:00 - 27:00 | 2:00 min)
% ------------------------------------------------------------------------------
slide14 :-
    format('~n================================================================================~n', []),
    format('SLIDE 14: PREVISÃO E EXECUÇÃO DOS SEIS CASOS (Etapa 8 | 25:00-27:00)~n', []),
    format('Apresentador: Jonas~n', []),
    format('================================================================================~n', []),
    format('+------+-------------------------------+----------+-----------+-----------------------------------+~n', []),
    format('| Caso | Consulta                      | Previsto | Executado | Justificativa / Diagnóstico       |~n', []),
    format('+------+-------------------------------+----------+-----------+-----------------------------------+~n', []),
    testar_caso('C01', acesso(ana, producao),          true,  'R05: F, C, T e S presentes'),
    testar_caso('C02', acesso(bruno, laboratorio),     false, 'R03: Falta treinamento (T=0)'),
    testar_caso('C03', acesso(carla, laboratorio),     true,  'R04: P, C, T e S presentes'),
    testar_caso('C04', acesso(diego, producao),        false, 'R06: Falta autorização especial (S=0)'),
    testar_caso('C05', acesso(elisa, laboratorio),     false, 'Visitante sem regra para laboratório'),
    testar_caso('C06', acesso(fernando, producao),     false, 'R05: Falta credencial válida (C=0)'),
    format('+------+-------------------------------+----------+-----------+-----------------------------------+~n~n', []),
    format('SÍNTESE DE ENCERRAMENTO DO BLOCO DO JONAS:~n', []),
    format('  * 100%% de aderência entre as predições lógicas e a execução computacional.~n', []),
    format('  * Atenção à distinção: C02, C04 e C06 possuem regra aplicável, mas faltou condição.~n', []),
    format('  * C05 (Elisa) NÃO POSSUI REGRA APLICÁVEL NA BASE (Visitante restrito à Recepção).~n', []),
    format('================================================================================~n~n', []).

testar_caso(CasoId, Consulta, Previsto, Justificativa) :-
    ( Consulta -> Executado = true ; Executado = false ),
    format('| ~w  | ~w~t~30| | ~w~t~9| | ~w~t~10| | ~w~t~34| |~n',
           [CasoId, Consulta, Previsto, Executado, Justificativa]).


% ------------------------------------------------------------------------------
% Apresentação Integrada Completa (Slides 10 ao 14 em sequência)
% ------------------------------------------------------------------------------
apresentar_tudo :-
    slide10,
    slide11,
    slide12,
    slide13,
    slide14.


% ==============================================================================
% ETAPA 11: MECANISMO DE ATIVAÇÃO E DESATIVAÇÃO DINÂMICA DO CASO C07 (GUSTAVO)
% ==============================================================================
% Permite demonstrar à banca examinadora o sistema ANTES e DEPOIS da inserção
% do novo caso criado pela equipe, sem precisar reiniciar o ambiente.
% ==============================================================================

ativar_c07 :-
    ( pessoa(gustavo) ->
        format('~n[C07 AVISO] Caso C07 (Gustavo) já está ATIVADO na base.~n', [])
    ;
        assertz(pessoa(gustavo)),
        assertz(funcionario(gustavo)),
        assertz(credencial_valida(gustavo)),
        assertz(treinamento_concluido(gustavo)),
        format('~n============================================================~n', []),
        format('[C07 ATIVADO COM SUCESSO]~n', []),
        format('Indivíduo: Gustavo cadastrado na base com os seguintes fatos:~n', []),
        format('  - pessoa(gustavo).~n', []),
        format('  - funcionario(gustavo).            (Categoria: Funcionário)~n', []),
        format('  - credencial_valida(gustavo).      (Condição C = Sim)~n', []),
        format('  - treinamento_concluido(gustavo).  (Condição T = Sim)~n', []),
        format('  * autorizacao_especial:            (Condição S = Não, ausente)~n', []),
        format('~nResultados esperados:~n', []),
        format('  ?- acesso(gustavo, laboratorio).   -> true  (Regra R03 satisfeita)~n', []),
        format('  ?- acesso(gustavo, producao).      -> false (Regra R05: falta autorização)~n', []),
        format('============================================================~n~n', [])
    ).

desativar_c07 :-
    ( \+ pessoa(gustavo) ->
        format('~n[C07 AVISO] Caso C07 (Gustavo) já está DESATIVADO da base.~n', [])
    ;
        retractall(pessoa(gustavo)),
        retractall(funcionario(gustavo)),
        retractall(prestador(gustavo)),
        retractall(visitante(gustavo)),
        retractall(credencial_valida(gustavo)),
        retractall(treinamento_concluido(gustavo)),
        retractall(autorizacao_especial(gustavo)),
        format('~n============================================================~n', []),
        format('[C07 DESATIVADO COM SUCESSO]~n', []),
        format('Todos os fatos relativos a Gustavo foram removidos da base.~n', []),
        format('A base retorna ao conjunto original de indivíduos (C01 a C06).~n', []),
        format('============================================================~n~n', [])
    ).

status_c07 :-
    format('~n============================================================~n', []),
    ( pessoa(gustavo) ->
        format('STATUS DO CASO C07: ATIVADO na base de conhecimento.~n', []),
        format('Fatos atuais de Gustavo:~n', []),
        ( funcionario(gustavo) -> format('  * funcionario: SIM~n', []) ; format('  * funcionario: NAO~n', []) ),
        ( credencial_valida(gustavo) -> format('  * credencial_valida: SIM~n', []) ; format('  * credencial_valida: NAO~n', []) ),
        ( treinamento_concluido(gustavo) -> format('  * treinamento_concluido: SIM~n', []) ; format('  * treinamento_concluido: NAO~n', []) ),
        ( autorizacao_especial(gustavo) -> format('  * autorizacao_especial: SIM~n', []) ; format('  * autorizacao_especial: NAO~n', []) )
    ;
        format('STATUS DO CASO C07: DESATIVADO (Gustavo não consta na base).~n', [])
    ),
    format('============================================================~n~n', []).

