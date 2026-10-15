% ==============================================================================
% SUÍTE DE TESTES AUTOMATIZADOS EM SWI-PROLOG (C01 A C07)
% ==============================================================================
% Arquivo: tests/test_casos.pl
% Execução: swipl -s tests/test_casos.pl -g run_tests -t halt
% ==============================================================================

:- consult('../src/atlas_access.pl').

run_tests :-
    format('~n============================================================~n', []),
    format('PROJETO ATLAS ACCESS - EXECUÇÃO DOS TESTES EM PROLOG~n', []),
    format('============================================================~n', []),
    test_c01,
    test_c02,
    test_c03,
    test_c04,
    test_c05,
    test_c06,
    format('~nTodos os testes da base original executados com sucesso!~n', []),
    format('============================================================~n', []).

test_c01 :-
    format('[C01] Ana / Produção: ', []),
    ( acesso(ana, producao) ->
        format('SUCESSO (true) - Conforme esperado (R05 satisfeito)~n', [])
    ;
        format('FALHA INESPERADA!~n', []), fail
    ).

test_c02 :-
    format('[C02] Bruno / Laboratório: ', []),
    ( \+ acesso(bruno, laboratorio) ->
        format('SUCESSO (false) - Conforme esperado (Falta treinamento para R03)~n', [])
    ;
        format('FALHA INESPERADA!~n', []), fail
    ).

test_c03 :-
    format('[C03] Carla / Laboratório: ', []),
    ( acesso(carla, laboratorio) ->
        format('SUCESSO (true) - Conforme esperado (R04 satisfeito)~n', [])
    ;
        format('FALHA INESPERADA!~n', []), fail
    ).

test_c04 :-
    format('[C04] Diego / Produção: ', []),
    ( \+ acesso(diego, producao) ->
        format('SUCESSO (false) - Conforme esperado (Falta autorização especial para R06)~n', [])
    ;
        format('FALHA INESPERADA!~n', []), fail
    ).

test_c05 :-
    format('[C05] Elisa / Laboratório: ', []),
    ( \+ acesso(elisa, laboratorio) ->
        format('SUCESSO (false) - Conforme esperado (Visitante sem regra de acesso)~n', [])
    ;
        format('FALHA INESPERADA!~n', []), fail
    ).

test_c06 :-
    format('[C06] Fernando / Produção: ', []),
    ( \+ acesso(fernando, producao) ->
        format('SUCESSO (false) - Conforme esperado (Falta credencial válida para R05)~n', [])
    ;
        format('FALHA INESPERADA!~n', []), fail
    ).
