% ==============================================================================
% PROJETO ATLAS ACCESS - BASE EVOLUÍDA (ETAPAS 10 E 11)
% ==============================================================================
% Instituição: Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe, São Carlos/SP
% Curso: Pós-Graduação Lato Sensu em Inteligência Artificial
% UCs Integradas: Lógica para Inteligência Artificial & Sistemas Baseados em Conhecimento
% Equipe: Fábio, Fabi, Jonas Poli, Luciano
% ==============================================================================
% Arquivo: src/atlas_access_evolucao.pl
% Descrição: Base evoluída incorporando:
%            - Etapa 10 Parte A: Alteração de fato (Bruno conclui treinamento).
%            - Etapa 10 Parte B: Nova política de acesso R07 (prestadores no Escritório).
%            - Etapa 11: Novo caso C07 criado pela equipe (Gustavo).
% ==============================================================================

% ==============================================================================
% SEÇÃO 1: FATOS DECLARADOS
% ==============================================================================

% --- Pessoas Cadastradas (Universo U) ---
% Inclui Gustavo (Caso C07 - Etapa 11)
pessoa(ana).
pessoa(bruno).
pessoa(carla).
pessoa(diego).
pessoa(elisa).
pessoa(fernando).
pessoa(gustavo).      % Novo indivíduo cadastrado (C07)

% --- Categorias de Pessoas ---
funcionario(ana).
funcionario(bruno).
funcionario(fernando).
funcionario(gustavo).  % Gustavo é funcionário

prestador(carla).
prestador(diego).

visitante(elisa).

% --- Condição C: Credencial Válida ---
credencial_valida(ana).
credencial_valida(bruno).
credencial_valida(carla).
credencial_valida(diego).
credencial_valida(elisa).
credencial_valida(gustavo). % Gustavo possui credencial válida

% --- Condição T: Treinamento Concluído ---
treinamento_concluido(ana).
treinamento_concluido(carla).
treinamento_concluido(diego).
treinamento_concluido(fernando).
treinamento_concluido(bruno).    % ALTERAÇÃO ETAPA 10 PARTE A: Bruno concluiu o treinamento!
treinamento_concluido(gustavo).  % Gustavo concluiu o treinamento

% --- Condição S: Autorização Especial emitida pela Segurança do Trabalho ---
% Gustavo NÃO possui autorização especial (portanto não consta aqui)
autorizacao_especial(ana).
autorizacao_especial(carla).
autorizacao_especial(fernando).


% ==============================================================================
% SEÇÃO 2: REGRAS DE ACESSO (R01 a R07)
% ==============================================================================

% --- R01: Recepção ---
acesso(X, recepcao) :-
    pessoa(X).

% --- R02: Escritório para Funcionários ---
acesso(X, escritorio) :-
    funcionario(X),
    credencial_valida(X).

% --- R03: Laboratório para Funcionários ---
acesso(X, laboratorio) :-
    funcionario(X),
    credencial_valida(X),
    treinamento_concluido(X).

% --- R04: Laboratório para Prestadores ---
acesso(X, laboratorio) :-
    prestador(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).

% --- R05: Produção para Funcionários ---
acesso(X, producao) :-
    funcionario(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).

% --- R06: Produção para Prestadores ---
acesso(X, producao) :-
    prestador(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).

% ------------------------------------------------------------------------------
% REGRA R07 - NOVA POLÍTICA (Etapa 10 Parte B)
% Trecho do comunicado: "A partir deste mês, prestadores de serviço com
%                       credencial válida e treinamento concluído também podem
%                       acessar o Escritório Administrativo."
% Formalização lógica: (P ∧ C ∧ T) -> AE
% Requisitos: Ser prestador E credencial válida E treinamento concluído.
% NOTA ARQUITETURAL: Adicionada modularmente sem necessidade de reescrever
% ou modificar nenhuma das regras pré-existentes (R01 a R06).
% ------------------------------------------------------------------------------
acesso(X, escritorio) :-
    prestador(X),
    credencial_valida(X),
    treinamento_concluido(X).
