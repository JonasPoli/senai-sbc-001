# ROTEIRO DE APRESENTAÇÃO · BLOCO DO JONAS (SLIDES 10 AO 14)
## Projeto Atlas Access · Pós-Graduação em Inteligência Artificial · SENAI São Carlos
**Integrantes:** Fábio, Fabi, **Jonas Poli**, Luciano  
**Tempo total do bloco:** 9 minutos (do minuto **18:00** ao minuto **27:00**)

---

## VISÃO GERAL DO SEU BLOCO

Você é o responsável por apresentar a **implementação prática, unificação, o motor de inferência em ação e a observação do trace** no Prolog. Este é o coração técnico da apresentação. A banca vai avaliar se você compreende a diferença entre execução procedural e dedução lógica declarativa, unificação sintática, o modelo de caixa de 4 portas (Byrd Box Model) e a Presunção de Mundo Fechado (CWA).

| Slide | Título | Etapas SA01 | Minutagem | Tempo |
|:---:|:---|:---:|:---:|:---:|
| **10** | Fatos, regras e inferência | 6 e 7 | 18:00 – 19:00 | 1:00 min |
| **11** | Regra Prolog e unificação | 6 e 7 | 19:00 – 21:00 | 2:00 min |
| **12** | Ana: uma prova bem-sucedida | 7 e 8 | 21:00 – 22:30 | 1:30 min |
| **13** | Diego: alternativas e falha | 7 e 8 | 22:30 – 25:00 | 2:30 min |
| **14** | Previsão e execução | 8 | 25:00 – 27:00 | 2:00 min |

---

## SLIDE 10 · Fatos, regras e inferência (18:00 – 19:00 | 1:00 min)

### O que mostrar na tela:
- Os 4 fatos positivos sobre Ana:
  ```prolog
  funcionario(ana).
  credencial_valida(ana).
  treinamento_concluido(ana).
  autorizacao_especial(ana).
  ```
- A consulta:
  ```prolog
  ?- acesso(ana, producao).
  ```

### O que falar (Roteiro de Fala):
> *"Obrigado, Fabi. Agora entramos na camada de implementação e raciocínio computacional com Prolog.*
> 
> *Aqui no Slide 10, temos a separação clássica de um Sistema Baseado em Conhecimento: de um lado, os fatos declarados na base; do outro, a consulta submetida ao motor de inferência.*
> 
> *Para a Ana, declaramos apenas os fatos positivos: ela é funcionária, possui credencial válida, treinamento concluído e autorização especial da Segurança do Trabalho. Note que a autorização de acesso da Ana NÃO está cadastrada diretamente como fato. Isso é proposital e fundamental: em um SBC, nós descrevemos o conhecimento do domínio por meio de regras, e não procedimentos estáticos. O motor de inferência é quem vai deduzir a elegibilidade de Ana buscando uma prova lógica a partir da regra R05."*

---

## SLIDE 11 · Regra Prolog e unificação (19:00 – 21:00 | 2:00 min)

### O que mostrar na tela:
- A regra R05 em formato de Cláusula de Horn:
  ```prolog
  acesso(X, producao) :-
      funcionario(X),
      credencial_valida(X),
      treinamento_concluido(X),
      autorizacao_especial(X).
  ```
- A tabela das 3 regras de unificação:
  | Regra de unificação | Exemplo | Significado Prático |
  |:---|:---|:---|
  | **Constantes iguais** | `ana` unifica com `ana`<br>`producao` com `producao` | Átomos/constantes só unificam se forem idênticos caractere por caractere. |
  | **Variável livre e termo** | `X` unifica com `ana` | A variável `X` (em maiúsculo) recebe o valor `ana` e substitui todo o corpo da regra por `ana`. |
  | **Estruturas compatíveis** | Mesmo predicado, aridade e argumentos | `acesso(..., ...)` casa com `acesso(..., ...)` porque ambos têm o mesmo nome e 2 argumentos. |

---

### 🧠 COMO ENTENDER ESSA TABELA (O "Mecanismo de Encaixe"):
Imagine que a consulta que você digitou é uma **chave** e a regra no arquivo é a **fechadura**:
```text
Sua Consulta (Pergunta):   acesso ( ana , producao )
                              │      │        │
                              ▼      ▼        ▼  (Comparação do Prolog)
Cabeça da Regra (Arquivo): acesso (  X  , producao ) :- funcionario(X), ...
```

O Prolog faz 3 verificações automáticas (as 3 linhas da sua tabela):

1. **Estruturas compatíveis:**
   - O nome do predicado é o mesmo? Sim: `acesso` com `acesso`.
   - O número de argumentos (aridade) é o mesmo? Sim: 2 argumentos de cada lado (`acesso/2`).
   - *Se fosse `acesso(ana)` com 1 argumento, ou `entrada(ana, producao)`, o Prolog já descartava imediatamente por incompatibilidade de estrutura.*

2. **Constantes iguais:**
   - O segundo argumento da sua pergunta é `producao` (em minúsculo, logo é uma constante/átomo).
   - O segundo argumento na regra é `producao`.
   - O Prolog compara: `producao == producao`? Sim! Constantes iguais unificam com sucesso.
   - *Se a regra fosse para o laboratório (`acesso(X, laboratorio)`), falharia aqui porque constante não casa com constante diferente.*

3. **Variável livre e termo:**
   - O primeiro argumento da sua pergunta é a constante `ana`.
   - O primeiro argumento na regra é a letra maiúscula `X` (uma variável livre, sem valor ainda).
   - O Prolog faz a amarração (ligação): `X = ana`.
   - **O efeito prático:** a partir desse momento, todas as ocorrências de `X` no corpo da regra são substituídas por `ana`:
     `funcionario(ana), credencial_valida(ana), treinamento_concluido(ana), autorizacao_especial(ana).`

---

### O que falar na apresentação (Roteiro de Fala Passo a Passo):

> *"Aqui no Slide 11, chegamos a um conceito fundamental do Prolog: como o motor de inferência sabe que a pergunta `acesso(ana, producao)` se aplica à regra R05?*
> 
> *A resposta é o algoritmo de **UNIFICAÇÃO SINTÁTICA**, que opera através das três regras demonstradas nesta tabela:*
> 
> *1. A primeira regra é a de **ESTRUTURAS COMPATÍVEIS**: o Prolog compara a assinatura da consulta com a cabeça da regra. Ambas possuem o mesmo predicado `acesso` e a mesma aridade de 2 argumentos — ou seja, `acesso/2` unifica com `acesso/2`.*
> 
> *2. A segunda regra é a de **CONSTANTES IGUAIS**: no segundo argumento, a constante `producao` que digitamos na consulta é idêntica à constante `producao` definida na regra, resultando em sucesso imediato.*
> 
> *3. A terceira regra é a de **VARIÁVEL LIVRE E TERMO**: na regra, o primeiro argumento é a variável maiúscula `X`, que está livre. O Prolog liga essa variável ao átomo `ana` (`X = ana`). E o efeito dessa amarração é propagado para todo o corpo da regra: agora o motor tem que provar `funcionario(ana)`, `credencial_valida(ana)`, `treinamento_concluido(ana)` e `autorizacao_especial(ana)`.*
> 
> *Além disso, o motor trabalha de forma determinística: ele sempre testa as cláusulas de **cima para baixo** no arquivo, e os objetivos do corpo da **esquerda para a direita**."*

---

## SLIDE 12 · Ana: uma prova bem-sucedida (21:00 – 22:30 | 1:30 min)

### O que mostrar na tela:
- O rastreamento de portas do Modelo de Caixa de 4 Portas de Byrd:
  - `Call: acesso(ana, producao)`
  - `Call: funcionario(ana)` -> `Exit: funcionario(ana)`
  - `Call: credencial_valida(ana)` -> `Exit: credencial_valida(ana)`
  - `Call: treinamento_concluido(ana)` -> `Exit: treinamento_concluido(ana)`
  - `Call: autorizacao_especial(ana)` -> `Exit: autorizacao_especial(ana)`
  - `Exit: acesso(ana, producao)` -> **true**

### O que falar (Roteiro de Fala):
> *"No Slide 12, abrimos a 'caixa preta' do motor de inferência através do modelo de 4 portas de Byrd.*
> 
> *Ao executarmos a consulta `acesso(ana, producao)`, o motor entra pela porta `Call`. Ele unifica com a regra R05 e passa a chamar sequencialmente cada sub-objetivo do corpo, da esquerda para a direita:*
> 1. *Chama `funcionario(ana)`: encontra o fato na base e sai pela porta `Exit`.*
> 2. *Chama `credencial_valida(ana)`: encontra o fato e sai por `Exit`.*
> 3. *Chama `treinamento_concluido(ana)`: também dá `Exit`.*
> 4. *Chama `autorizacao_especial(ana)`: também dá `Exit`.*
> 
> *Como todos os sub-objetivos foram provados sem nenhuma falha, a consulta principal sai vitoriosa pela porta `Exit` e o Prolog retorna `true`.*
> 
> *Destaque importante para a banca: no caso da Ana, NÃO houve nenhum backtracking, pois o primeiro ramo da árvore de busca foi suficiente para construir a prova."*

---

## SLIDE 13 · Diego: alternativas e falha (22:30 – 25:00 | 2:30 min)

### O que mostrar na tela:
- Tabela de passos com a porta `Redo` e o backtracking ocorrendo entre R05 e R06:
  1. `funcionario(diego)` em R05 -> `Call -> Fail`
  2. `acesso(diego, producao)` -> `Redo` (Backtracking para regra R06)
  3. `prestador(diego)` -> `Call -> Exit`
  4. `credencial_valida(diego)` -> `Call -> Exit`
  5. `treinamento_concluido(diego)` -> `Call -> Exit`
  6. `autorizacao_especial(diego)` -> `Call -> Fail`
  7. `acesso(diego, producao)` -> `Fail (false)`

### O que falar (Roteiro de Fala):
> *"Agora, no Slide 13, analisamos um caso muito mais rico e revelador: a solicitação de Diego para a Produção.*
> 
> *O Diego é prestador de serviço, tem credencial e treinamento, mas NÃO tem autorização especial. Observem o comportamento do motor:*
> 
> *Primeiro, seguindo a ordem de cima para baixo, o Prolog tenta a primeira regra de produção que encontra no arquivo, que é a R05 (voltada a funcionários). Ele chama `funcionario(diego)`. Como Diego é prestador, esse objetivo falha imediatamente e sai pela porta `Fail`.*
> 
> *É aqui que entra o BACKTRACKING: ao falhar em R05, o motor não desiste! Ele volta pela porta `Redo` ao objetivo `acesso(diego, producao)` e procura no arquivo a próxima regra aplicável. Ele encontra a regra R06, destinada a prestadores!*
> 
> *Em R06, ele avança com sucesso: `prestador(diego)` dá Exit, `credencial_valida(diego)` dá Exit, `treinamento_concluido(diego)` dá Exit. Porém, ao chamar `autorizacao_especial(diego)`, essa condição NÃO está na base. Ocorre um `Fail`.*
> 
> *Como não existem outras cláusulas para a Produção no arquivo, o motor esgota as alternativas e retorna `false`.*
> 
> *Atenção especial à interpretação deste resultado: segundo a Presunção de Mundo Fechado (Closed World Assumption), `false` no Prolog não é uma prova matemática de falsidade no universo; significa estritamente que a hipótese não é demonstrável com a base de conhecimento atual."*

---

## SLIDE 14 · Previsão e execução (25:00 – 27:00 | 2:00 min)

### O que mostrar na tela:
- A matriz comparativa dos 6 casos obrigatórios:
  - C01 (Ana / Produção): Previsto `true` / Executado `true`
  - C02 (Bruno / Laboratório): Previsto `false` / Executado `false` (falta T)
  - C03 (Carla / Laboratório): Previsto `true` / Executado `true`
  - C04 (Diego / Produção): Previsto `false` / Executado `false` (falta S)
  - C05 (Elisa / Laboratório): Previsto `false` / Executado `false` (Visitante sem regra)
  - C06 (Fernando / Produção): Previsto `false` / Executado `false` (falta C - crachá vencido)

### O que falar (Roteiro de Fala):
> *"Para fechar o meu bloco, o Slide 14 apresenta a validação experimental completa entre o que deduzimos na lógica e o que o Prolog executou nos seis casos obrigatórios.*
> 
> *Obtivemos 100% de convergência entre as previsões teóricas e a execução do código.*
> 
> *Mas o ponto mais sutil e conceitual que a nossa equipe registrou nesta etapa é a natureza das respostas `false`:*
> - *Nos casos C02, C04 e C06, EXISTE uma regra aplicável no sistema, mas falta uma condição fática específica: para o Bruno falta treinamento; para o Diego falta autorização especial; e para o Fernando falta credencial válida (crachá vencido).*
> - *Já no caso C05 da Elisa, a situação é estruturalmente diferente: a Elisa é Visitante, e segundo a IT-SEG-014, visitantes só acessam a Recepção. Portanto, NÃO EXISTE NENHUMA REGRA no sistema que autorize visitante no laboratório.*
> 
> *Essa distinção entre 'falta de condição' e 'ausência de regra' é essencial para que o sistema consiga emitir justificativas claras e auditáveis ao usuário.*
> 
> *Agora passo a palavra ao Luciano, que vai demonstrar como essas decisões lógicas acionam a evolução dos estados na Máquina de Estados da solicitação. Obrigado!"*

---

## COMANDOS PRÁTICOS PARA DEMONSTRAR AO VIVO

### Opção 1: Demonstração Rápida em Python (Recomendada!)
Abra o terminal na pasta do projeto e execute:
```bash
# Apresentação completa interativa com pausas slide a slide:
python3 apresentacao_jonas.py

# Ou se quiser mostrar um slide específico:
python3 apresentacao_jonas.py 12   # Mostra o trace da Ana
python3 apresentacao_jonas.py 13   # Mostra o backtracking do Diego
python3 apresentacao_jonas.py 14   # Mostra a tabela de validação
```

### Opção 2: Demonstração Direta no SWI-Prolog
Caso o professor peça para abrir o `swipl`:
```bash
swipl slides_10_a_14.pl
```
Dentro do terminal do Prolog, digite:
```prolog
?- slide10.
?- slide11.
?- slide12.
?- slide13.
?- slide14.

% Ou se o professor quiser ver o trace interativo nativo do SWI-Prolog:
?- trace, acesso(ana, producao), notrace.
?- trace, acesso(diego, producao), notrace.
```

---

## PERGUNTAS QUE O PROFESSOR PODE FAZER A VOCÊ E COMO RESPONDER

### Pergunta 1: *"Jonas, por que o Prolog retornou 'false' para o Fernando se ele tem autorização especial e treinamento?"*
> **Sua Resposta:** *"Professor, o Fernando tem treinamento e autorização especial, mas a regra R05 exige conjuntamente que a credencial seja válida. No texto da IT-SEG-014, o especialista enfatizou que 'crachá vencido não entra em área controlada de jeito nenhum'. Como o Fernando está com credencial inválida, o fato `credencial_valida(fernando)` não consta na nossa base. Sob a Presunção de Mundo Fechado, o objetivo falha e a regra não pode ser demonstrada."*

### Pergunta 2: *"Jonas, se nós trocássemos a ordem das regras R05 e R06 no arquivo, mudaria o resultado final de Diego?"*
> **Sua Resposta:** *"O resultado final continuaria sendo `false`, porque Diego não possui autorização especial e ambas as regras exigem essa condição. Porém, a ORDEM DO TRACE mudaria: se R06 estivesse antes de R05, o motor tentaria R06 primeiro, unificaria `prestador`, `credencial` e `treinamento`, falharia em `autorizacao_especial`, e só então faria backtracking para tentar R05, onde falharia em `funcionario`. A ordem das cláusulas altera o caminho da busca em profundidade, embora preserve o resultado dedutivo."*

### Pergunta 3: *"Jonas, qual a diferença conceitual entre o caso de Elisa (C05) e o de Diego (C04)?"*
> **Sua Resposta:** *"No caso de Diego, ele pertence a uma categoria prevista pela regra R06 (prestador), mas falhou por falta de uma condição fática (`autorizacao_especial`). Já no caso de Elisa, ela é visitante, e na IT-SEG-014 não existe nenhuma política que conceda acesso de visitante a áreas controladas. Ou seja, em Elisa não faltou apenas um fato; faltou uma regra que sustentasse a dedução. Isso é crucial para a trilha de explicação ao usuário."*

### Pergunta 4: *"Jonas, como vocês ativam e desativam o novo caso criado (C07 - Gustavo) para comparar o comportamento do sistema?"*
> **Sua Resposta:** *"Professor, implementamos quatro formas de alternância:  
> 1. Diretamente no REPL do Prolog usando os predicados dinâmicos `ativar_c07.` e `desativar_c07.` via `assertz` e `retractall`;  
> 2. Pelo nosso painel interativo `main.py`, onde a tecla `T` alterna o C07 na matriz em tempo real;  
> 3. Pelo comando `python3 apresentacao_jonas.py --c07`, que roda o ciclo completo de antes e depois;  
> 4. Ou carregando a base estática original `atlas_access.pl` versus a base evoluída `atlas_access_evolucao.pl`."*

---

## GUIA RÁPIDO: COMO ATIVAR / DESATIVAR O CASO C07 AO VIVO

### 1. No SWI-Prolog:
```prolog
?- status_c07.       % Mostra o status atual
?- ativar_c07.       % Adiciona Gustavo na base (F=1, C=1, T=1, S=0)
?- acesso(gustavo, laboratorio).  % true
?- acesso(gustavo, producao).     % false
?- desativar_c07.    % Remove Gustavo da base (retorna à base original)
```

### 2. No Terminal via Python:
```bash
# Demonstração rápida dos 3 momentos (sem C07, ativado, desativado):
python3 apresentacao_jonas.py --c07

# No painel geral (pressione T para alternar e 1 para ver a matriz):
python3 main.py
```


