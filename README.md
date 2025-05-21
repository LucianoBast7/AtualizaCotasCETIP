# AtualizaCotas – Atualização de Cotas e Envio para CETIP

## 📌 Visão Geral

Este projeto automatiza a captura, comparação, filtragem e envio de dados de cotas de fundos entre diferentes fontes (Sinqia e VxCotas), com verificação de dias úteis e envio automatizado ao portal CETIP via Selenium.

---

## 🔧 Funcionalidades

- Verificação automática de dia útil com Workalendar.
- Captura de dados de cotas via SQL Server e PostgreSQL.
- Cruzamento e filtragem entre dados da Sinqia e VxCotas.
- Atualização da base de processamento apenas com registros novos.
- Geração de layout `.txt` no padrão CETIP.
- Acesso e envio automatizado ao portal CETIP.
- Registro completo em arquivos de log.

---

## ⚙️ Tecnologias Utilizadas

- **Python**
- **Selenium WebDriver**
- **pandas / numpy**
- **pyodbc / SQLAlchemy**
- **Workalendar**
- **PostgreSQL / SQL Server**

---

## 🗂️ Estrutura do Projeto

- `AtualizaCotas.py`: script principal de execução.
- `sql.py`: manipulação de dados SQL (consulta, comparação, envio).
- `layout.py`: geração do layout CETIP.
- `importa.py`: automação da importação no portal CETIP.
- `calendar.py`: verificação de dias úteis com base em feriados brasileiros.
- `log.py`: configuração de logs detalhados por execução.
- `queries.py`: definições das queries Sinqia e VxCotas.
- `variaveis.py`: carregamento de variáveis de ambiente.
- `funcoes_selenium.py`: automações genéricas via Selenium.

---

## 🔐 Variáveis Sensíveis

Configuradas via `.env` e carregadas por:
```
requirements/variaveis/variaveis.py
```

Variáveis:
- Acessos a bancos de dados (Sinqia, VxCotas, Automate)
- Acesso ao portal CETIP
- Caminho dinâmico do arquivo de exportação

---

## 🚀 Como Executar

1. Certifique-se de configurar o arquivo `.env` com as credenciais e caminhos.
2. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```
3. Execute o script principal:
```bash
python AtualizaCotas.py
```

---

## 📁 Saídas Geradas

- `LayoutCetip.txt`: arquivo formatado com cotas para importação.
- Registro na tabela `tbProcessPY018` (base interna).
- Logs diários em `W:\PY_018 - Atualiza Cotas CETIP\0. Log\{ano}\{mes}\{dia}\`.

---

## ⚠️ Observações

- Execução bloqueada automaticamente em dias não úteis.
- Layout CETIP segue rigorosamente o padrão exigido.
- Apenas dados novos são processados e enviados.

---

## 🤝 Contribuições

Sugestões, melhorias e correções são bem-vindas. Colabore com este projeto por meio de issues ou pull requests.

