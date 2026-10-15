% ==============================================================================
% PROJETO ATLAS ACCESS - SISTEMA BASEADO EM CONHECIMENTO (SBC)
% ==============================================================================
% Instituição: Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe, São Carlos/SP
% Curso: Pós-Graduação Lato Sensu em Inteligência Artificial
% UCs Integradas: Lógica para Inteligência Artificial & Sistemas Baseados em Conhecimento
% Situação de Aprendizagem 01 (SA01) - Controle de Acesso a Áreas Industriais
% Equipe: Fábio, Fabi, Jonas Poli, Luciano
% ==============================================================================
% Arquivo: src/atlas_access.pl
% Descrição: Base de conhecimento original contendo fatos positivos declarados
%            e regras operacionais de acesso (R01 a R06) extraídas da IT-SEG-014.
% ==============================================================================

% ==============================================================================
% SEÇÃO 1: FATOS DECLARADOS (Universo e Condições Iniciais)
% ==============================================================================
% NOTA SOBRE A PRESUNÇÃO DE MUNDO FECHADO (CWA):
% Apenas fatos positivos verdadeiros são explicitamente declarados na base.
% Condições com valor "Não" na tabela do projeto (ex.: Fernando sem credencial
% válida, Diego sem autorização especial) NÃO são declaradas. O motor de
% inferência interpretará a ausência de prova como não demonstrável, e não
% como uma negação lógica formal comprovada no mundo real.
% ==============================================================================

% --- Pessoas Cadastradas (Universo U) ---
pessoa(ana).
pessoa(bruno).
pessoa(carla).
pessoa(diego).
pessoa(elisa).
pessoa(fernando).

% --- Categorias de Pessoas ---
% Funcionários (F)
funcionario(ana).
funcionario(bruno).
funcionario(fernando).

% Prestadores de Serviço (P)
prestador(carla).
prestador(diego).

% Visitantes (V)
visitante(elisa).

% --- Condição C: Credencial Válida ---
% "Reforçando: crachá vencido não entra em área controlada de jeito nenhum."
% Fernando possui crachá vencido / credencial inválida, portanto NÃO consta aqui.
credencial_valida(ana).
credencial_valida(bruno).
credencial_valida(carla).
credencial_valida(diego).
credencial_valida(elisa).

% --- Condição T: Treinamento Concluído ---
% Bruno e Elisa não concluíram o treinamento, portanto NÃO constam aqui.
treinamento_concluido(ana).
treinamento_concluido(carla).
treinamento_concluido(diego).
treinamento_concluido(fernando).

% --- Condição S: Autorização Especial emitida pela Segurança do Trabalho ---
% Bruno, Diego e Elisa não possuem autorização especial, portanto NÃO constam aqui.
autorizacao_especial(ana).
autorizacao_especial(carla).
autorizacao_especial(fernando).


% ==============================================================================
% SEÇÃO 2: REGRAS DE ACESSO (Políticas Operacionais R01 a R06)
% ==============================================================================
% Formato: acesso(Pessoa, Area).
% As regras formalizam as condições suficientes extraídas da IT-SEG-014.
% ==============================================================================

% ------------------------------------------------------------------------------
% REGRA R01 - Recepção (Área A01)
% Trecho da fonte: "A Recepção é área de livre atendimento e os visitantes
%                  permanecem nela durante toda a estadia."
% Formalização lógica: U -> AR
% Requisitos: Qualquer pessoa cadastrada no sistema. Nenhum requisito C, T ou S.
% ------------------------------------------------------------------------------
acesso(X, recepcao) :-
    pessoa(X).

% ------------------------------------------------------------------------------
% REGRA R02 - Escritório Administrativo (Área A02)
% Trecho da fonte: "O Escritório Administrativo é destinado ao pessoal próprio:
%                  qualquer funcionário da casa que esteja com a credencial
%                  válida pode entrar."
% Formalização lógica: (F ∧ C) -> AE
% Requisitos: Ser funcionário E possuir credencial válida.
% ------------------------------------------------------------------------------
acesso(X, escritorio) :-
    funcionario(X),
    credencial_valida(X).

% ------------------------------------------------------------------------------
% REGRA R03 - Laboratório Técnico (Área A03) para Funcionários
% Trecho da fonte: "No Laboratório, além da credencial, exigimos o treinamento
%                  concluído para os funcionários..."
% Formalização lógica: (F ∧ C ∧ T) -> AL
% Requisitos: Ser funcionário E credencial válida E treinamento concluído.
% ------------------------------------------------------------------------------
acesso(X, laboratorio) :-
    funcionario(X),
    credencial_valida(X),
    treinamento_concluido(X).

% ------------------------------------------------------------------------------
% REGRA R04 - Laboratório Técnico (Área A03) para Prestadores de Serviço
% Trecho da fonte: "...para prestadores de serviço, além do treinamento, exigimos
%                  também a autorização especial emitida pela Segurança do
%                  Trabalho."
% Formalização lógica: (P ∧ C ∧ T ∧ S) -> AL
% Requisitos: Ser prestador E credencial válida E treinamento concluído E autorização especial.
% ------------------------------------------------------------------------------
acesso(X, laboratorio) :-
    prestador(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).

% ------------------------------------------------------------------------------
% REGRA R05 - Área de Produção (Área A04) para Funcionários
% Trecho da fonte: "Na Área de Produção o critério é o mais rigoroso: credencial,
%                  treinamento e autorização especial, e isso vale igualmente
%                  para funcionários e para prestadores."
% Formalização lógica: (F ∧ C ∧ T ∧ S) -> AP
% Requisitos: Ser funcionário E credencial válida E treinamento concluído E autorização especial.
% ------------------------------------------------------------------------------
acesso(X, producao) :-
    funcionario(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).

% ------------------------------------------------------------------------------
% REGRA R06 - Área de Produção (Área A04) para Prestadores de Serviço
% Trecho da fonte: "...e isso vale igualmente para funcionários e para prestadores."
% Formalização lógica: (P ∧ C ∧ T ∧ S) -> AP
% Requisitos: Ser prestador E credencial válida E treinamento concluído E autorização especial.
% ------------------------------------------------------------------------------
acesso(X, producao) :-
    prestador(X),
    credencial_valida(X),
    treinamento_concluido(X),
    autorizacao_especial(X).
