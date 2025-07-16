# Documentação Padrão de Desenvolvimento RPA em Python (Projeto Base: PY\_018 - Atualiza Cotas CETIP)

## 1. Finalidade do Documento

Esta documentação visa padronizar a estrutura e boas práticas de desenvolvimento para projetos de RPA em Python, utilizando o projeto "**PY\_018 - Atualiza Cotas CETIP**" como base de referência. A padronização facilita a manutenção, expansão e compreensão dos scripts por diferentes desenvolvedores.

---

## 2. Estrutura do Projeto

```
PY_018 - Atualiza Cotas CETIP/
└─7. Scripts/
   ├── AtualizaCotas.py               # Arquivo orquestrador principal
   ├── log/
   │   └── log.py                     # Gerenciamento de logs
   ├── requirements/
       ├── variaveis/
       │   └── variaveis.py           # Variáveis sensíveis e de ambiente
       ├── selenium/
       │   └── funcoes_selenium.py     # Funções genéricas com Selenium
       ├── requirements/
       │   ├── requirements.txt       # Dependências do projeto
       │   ├── .python-version         # Versão do interpretador Python
       │   └── tbProcessamento.sql     # Script de criação da tabela de processamento
       ├── queries/
       │   └── queries.py              # Definição de queries SQL
       ├── config/
           ├── calendar.py             # Validação de dia útil
           ├── importa.py              # Controle de importação no sistema externo
           ├── layout.py               # Criação de arquivo de layout
           └── sql.py                  # Funções de conexão e manipulação em SQL
```

---

## 3. Estrutura do Arquivo Orquestrador (`AtualizaCotas.py`)

Responsável por orquestrar todo o fluxo do RPA:

* Verifica se é dia útil
* Captura dados de origem (Sinqia e VxCotas)
* Compara, casa e filtra os dados
* Atualiza base de processamento
* Gera arquivo de layout
* Realiza importação no sistema CETIP via automação web (Selenium)
* Loga todas as etapas

**Motivo da estrutura:** garantir separação clara de responsabilidades, facilitando depuração e reaproveitamento de componentes.

---

## 4. Estrutura de Logs (`log/log.py`)

* Cada execução gera um arquivo de log com data, nomeado como `AtualizaCotasCETIP_<data>.log`
* Armazenado em: `W:/PY_018 - Atualiza Cotas CETIP/0. Log/ano/mes/dia`
* Utiliza o módulo `logging` do Python com log level configurável

**Motivo da estrutura:** permite rastreabilidade detalhada e organização cronológica.

---

## 5. Estrutura de Conexão com Banco e Queries (`config/sql.py` e `queries/queries.py`)

* SQL Server (via pyodbc) e PostgreSQL (via SQLAlchemy)
* Conexões seguras usando dados carregados dinamicamente de `.env`
* Querys separadas por função (módulo `queries.py`)
* Funções reutilizáveis como `executa_query`, `casa_dados`, `registros_atualizados`, `envia_processamento`

**Motivo da estrutura:** separação clara de lógica de negócio e dados, facilitando manutenção e testes.

---

## 6. Estrutura de Geração de Layout (`config/layout.py`)

* Cria arquivo `.txt` em formato CETIP
* Inclui cabeçalho e linhas de dados formatadas conforme padrão

**Motivo da estrutura:** garantir compatibilidade com o sistema externo e centralizar formatações.

---

## 7. Estrutura de Automação Selenium (`selenium/funcoes_selenium.py`, `config/importa.py`)

* Abstração de comandos Selenium no `SeleniumAutomator`
* `importa.py` orquestra a navegação no portal CETIP e realiza o upload do arquivo
* Diretório de salvamento de PDF definido automaticamente por data

**Motivo da estrutura:** reutilização de funções e isolação da lógica de interação web.

---

## 8. Estrutura de Validação de Data Útil (`config/calendar.py`)

* Usa biblioteca `workalendar` para considerar feriados brasileiros e verificar se a data atual é dia útil
* Aborta execução se não for

**Motivo da estrutura:** evita execuções desnecessárias fora do expediente ou em feriados.

---

## 9. Estrutura de Variáveis e Caminhos (`variaveis/variaveis.py`)

* Utiliza `dotenv` para carregar credenciais e caminhos sensíveis
* Define dinamicamente diretório de arquivo com base na data da execução

**Motivo da estrutura:** segurança e flexibilidade para ambientes distintos (dev/hml/prd).

---

## 10. Estrutura da Tabela SQL (`tbProcessamento.sql`)

```sql
CREATE TABLE AutomateEnterprise.dbo.tbProcessPY018 (
    id INT IDENTITY(1,1) PRIMARY KEY,
    TipoIF VARCHAR(100),
    CodigoIF VARCHAR(100),
    DataValor DATETIME DEFAULT GETDATE(),
    ValorCota DECIMAL(20,8),
    CnpjFundo VARCHAR(30),
    DataProcessamento DATETIME DEFAULT GETDATE()
);
```

**Motivo da estrutura:** permite controle de duplicidade, histórico de execuções e reprocessamentos.

---

## 11. Considerações Finais

Este padrão deve ser adotado como referência para futuros projetos de RPA desenvolvidos em Python, com foco em:

* Clareza na separação de responsabilidades
* Modularização e reutilização de componentes
* Padronização de logs e nomenclatura
* Segurança de credenciais e dados sensíveis
* Facilidade para testes, manutenção e onboarding de novos desenvolvedores

> **Sugestão:** manter um repositório Git com esse modelo base, versionando atualizações por projeto.
