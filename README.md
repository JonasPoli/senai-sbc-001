# Projeto Atlas Access · Sistema Baseado em Conhecimento (SBC)

> **Controle de Acesso a Áreas Industriais com Regras Lógicas, Prolog e Máquina de Estados**  
> **Curso:** Pós-Graduação Lato Sensu em Inteligência Artificial  
> **Unidades Curriculares Integradas:** Lógica para IA & Sistemas Baseados em Conhecimento  
> **Instituição:** Faculdade de Tecnologia SENAI Antonio Adolpho Lobbe · São Carlos/SP  
> **Equipe do Projeto:** Fábio, Fabi, **Jonas Poli**, Luciano  

---

## 📂 Estrutura de Arquivos Organizada por Utilidade

O projeto está 100% categorizado em pastas dedicadas, pronto para execução no **Windows**, **Mac** e **Linux**:

```text
senai-prolog/
│
├── 📁 prolog/                       <-- [TUDO EM PROLOG · .pl]
│   ├── atlas_access.pl              (⭐ BASE PRINCIPAL: Regras R01 a R06 e fatos originais)
│   ├── atlas_access_evolucao.pl     (Base com as Etapas 10 e 11: Bruno treinado e C07 Gustavo)
│   ├── atlas_access_explicador.pl   (Motor nativo de explicações em linguagem natural)
│   ├── apresentacao_slides.pl       (Apresentação interativa dos slides via terminal Prolog)
│   └── test_casos.pl                (Suíte de testes automatizados em Prolog puro)
│
├── 📁 python/                       <-- [TUDO EM PYTHON · .py]
│   ├── apresentacao_jonas.py        (Simulador e ensaio interativo dos slides 10 ao 14)
│   ├── main.py                      (Console geral do sistema com menu interativo 1 a 9)
│   ├── state_machine.py             (Máquina de Estados FSM da solicitação de acesso)
│   ├── engine/                      (Motor de Inferência SLD, Tabela-Verdade e Explicador)
│   └── tests/test_suite.py          (12 testes unitários automatizados em Python)
│
├── 📁 slides_html/                  <-- [TUDO EM HTML/SVG · SLIDES]
│   ├── apresentacao_slides_jonas.html (Visualizador mestre com abas e botão de copiar)
│   ├── slide10_fatos_inferencia.html
│   ├── slide11_unificacao.html
│   ├── slide12_ana_prova.html
│   ├── slide13_diego_backtracking.html
│   ├── slide14_previsao_execucao.html
│   └── slide11.svg
│
├── 📁 documentos/                   <-- [TUDO EM MARKDOWN E PDF · DOCUMENTAÇÃO]
│   ├── ROTEIRO_APRESENTACAO_JONAS.md(Roteiro minuto a minuto e defesas da banca)
│   ├── DOSSIE_TECNICO.md            (Dossiê acadêmico completo das 12 etapas)
│   ├── SA01_Access.pdf              (Enunciado original do projeto)
│   └── Atlas Access · Apresentação.pdf (PDF oficial dos 40 minutos)
│
├── executar_windows.bat             <-- [LANÇADOR WINDOWS: 2 cliques para abrir menu]
└── README.md                        <-- Guia rápido de execução
```

---

## 🪟 Como Rodar no Windows

### Método 1: Dois Cliques (O Mais Fácil)
Basta dar **dois cliques no arquivo `executar_windows.bat`**.  
Um menu em português aparecerá no terminal permitindo:
* Abrir o SWI-Prolog direto com a base `prolog/atlas_access.pl`.
* Abrir o ensaio interativo em Python.
* Executar a suíte de testes.
* Abrir o visualizador de slides no navegador.

### Método 2: Via Linha de Comando (Prompt de Comando ou PowerShell)

#### 1. Usando SWI-Prolog (Windows, Mac ou Linux):
```bash
# Abrir a base principal no SWI-Prolog:
swipl prolog/atlas_access.pl

# No prompt interativo ?- digite:
?- acesso(ana, producao).
true.

?- acesso(diego, producao).
false.

?- halt.
```

Para rodar a apresentação dos slides 10 a 14 no SWI-Prolog:
```bash
swipl prolog/apresentacao_slides.pl
# No prompt ?- digite: slide10. ou slide12. ou slide13. ou slide14.
```

Para rodar os testes em Prolog:
```bash
swipl -s prolog/test_casos.pl -g run_tests -t halt
```

#### 2. Usando Python:
```bash
# Ensaio da apresentação dos slides do Jonas (10 ao 14):
python3 python/apresentacao_jonas.py

# Executar apenas um slide específico:
python3 python/apresentacao_jonas.py 12
python3 python/apresentacao_jonas.py 13
python3 python/apresentacao_jonas.py 14

# Menu geral interativo:
python3 python/main.py

# Executar os 12 testes unitários:
python3 -m unittest python/tests/test_suite.py
```
*(No Windows, se `python3` não estiver definido, use `python` no lugar de `python3`).*

---

## 🍎 Como Rodar no Mac / Linux

```bash
# Apresentação do Jonas em Python:
python3 python/apresentacao_jonas.py

# SWI-Prolog:
swipl prolog/atlas_access.pl

# Testes automatizados:
python3 -m unittest python/tests/test_suite.py
```

---

## 📋 Como Copiar as Tabelas para o Google Slides

1. Abra o arquivo `slides_html/apresentacao_slides_jonas.html` no seu navegador (Chrome/Edge/Safari).
2. Escolha o slide desejado (Slide 10 ao 14).
3. Clique no botão **"📋 Copiar Tabela Atual (Google Slides)"**.
4. No Google Slides, selecione o slide correspondente e pressione **`Ctrl+V`** (Windows) ou **`Cmd+V`** (Mac).
5. A tabela é colada como uma tabela nativa e formatada do Google Slides!
