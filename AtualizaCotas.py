from datetime import datetime, date
import warnings
warnings.filterwarnings("ignore")
from requirements.variaveis.variaveis import ConfigVaraveies
from requirements.queries.queries import ConfigQueries
from requirements.config.sql import ConfigSQL
from log.log import ConfigLog
from requirements.config.layout import ConfigLayout
from requirements.config.importa import ConfigImport
from requirements.config.calendar import ConfigCalendar, VortxCalendar

# Carregando Configs
variaveis = ConfigVaraveies()
queries = ConfigQueries()
sql = ConfigSQL()
log = ConfigLog()
layout = ConfigLayout()
bot = ConfigImport()
calendar = VortxCalendar()
iwd = ConfigCalendar()

# VERIFICA DIA UTIL
print(f"{datetime.now()} - VERIFICANDO DIA ÚTIL")
log.add_log("VERIFICANDO DIA ÚTIL")
iwd.verifica_dia_util(calendar, log)
print(f"{datetime.now()} - HOJE É DIA ÚTIL, INICIANDO EXECUÇÃO...")
log.add_log("HOJE É DIA ÚTIL, INICIANDO EXECUÇÃO...")

# CAPTURA DADOS IF DO SINQIA
print(f"{datetime.now()} - CAPTURA DADOS IF DO SINQIA")
log.add_log("CAPTURA DADOS IF DO SINQIA")
dados_sinqia = sql.executa_query(queries.query_sinqia(), variaveis.host_sinqia, variaveis.database_sinqia, variaveis.user_sinqia, variaveis.password_sinqia, log)
print(f"{datetime.now()} - DADOS IF CAPTURADOS: ({len(dados_sinqia)})")
log.add_log(f"DADOS IF CAPTURADOS: ({len(dados_sinqia)})")

# CRIA LISTA CNPJ
print(f"{datetime.now()} - CRIA LISTA CNPJ")
log.add_log("CRIA LISTA CNPJ")
lista_cnpj = sql.lista_cnpj(dados_sinqia, log)
print(f"{datetime.now()} - LISTA CNPJ CRIADA: ({len(lista_cnpj)})")
log.add_log(f"LISTA CNPJ CRIADA: ({len(lista_cnpj)})")

# CAPTURA DADOS VXCOTAS
print(f"{datetime.now()} - CAPTURA DADOS VXCOTAS")
log.add_log("CAPTURA DADOS VXCOTAS")
dados_vxcotas = sql.executa_query_vxcotas(queries.query_vxcotas(lista_cnpj, date.today()), variaveis.host_vxcotas, variaveis.database_vxcotas, variaveis.user_vxcotas, variaveis.password_vxcotas, log)
print(f"{datetime.now()} - DADOS VXCOTAS CAPTURADOS: ({len(dados_vxcotas)})")
log.add_log(f"DADOS VXCOTAS CAPTURADOS: ({len(dados_vxcotas)})")

# CASANDO DADOS
print(f"{datetime.now()} - CASANDO DADOS IF X VXCOTAS")
log.add_log("CASANDO DADOS IF X VXCOTAS")
dados_casados = sql.casa_dados(dados_vxcotas, dados_sinqia, log)
print(f"{datetime.now()} - DADOS CASADOS: ({len(dados_casados)})")
log.add_log(f"DADOS CASADOS: ({len(dados_casados)})")

# VERIFICA REGISTROS PROCESSADOS
print(f"{datetime.now()} - FILTRA DADOS COM REGISTROS DA BASE")
log.add_log("FILTRA DADOS COM REGISTROS DA BASE")
dados_filtrados = sql.registros_atualizados(dados_casados, variaveis.host_automate, variaveis.database_automate, variaveis.user_automate, variaveis.password_automate, log)
print(f"{datetime.now()} - DADOS FILTRADOS")
log.add_log(f"DADOS FILTRADOS")

# ATUALIZA BASE PROCESSAMENTO
print(f"{datetime.now()} - ATUALIZA BASE PROCESSAMENTO")
log.add_log("ATUALIZA BASE PROCESSAMENTO")
dados_enviados = sql.envia_processamento(dados_filtrados, variaveis.host_automate, variaveis.database_automate, variaveis.user_automate, variaveis.password_automate, log)
print(f"{datetime.now()} - {dados_enviados}")
log.add_log(f"{dados_enviados}")

# CRIA LAYOUT CETIP
print(f"{datetime.now()} - CRIA LAYOUT CETIP")
log.add_log(f"CRIA LAYOUT CETIP")
arquivo_cetip = layout.criar_layout(dados_filtrados, dados_enviados, variaveis.arquivo_cetip, log)
print(f"{datetime.now()} - LAYOUT CRIADO")
log.add_log(f"LAYOUT CRIADO")

# IMPORTA CETIP
print(f"{datetime.now()} - INICIANDO PORTAL CETIP")
log.add_log("INICIANDO PORTAL CETIP")
inicia_cetip = bot.acessar_cetip(variaveis.empresa_cetip, variaveis.user_cetip, variaveis.password_cetip, log)
print(f"{datetime.now()} - PORTAL ABERTO")
log.add_log("PORTAL ABERTO")

# ACESSA ABA IMPORTACAO
print(f"{datetime.now()} - ACESSA ABA IMPORTACAO")
log.add_log("ACESSA ABA IMPORTACAO")
acessa_aba = bot.acessar_trans_arquivo(log)
print(f"{datetime.now()} - ABA ABERTA")
log.add_log("ABA ABERTA")

# IMPORTA ARQUIVO
print(f"{datetime.now()} - IMPORTA ARQUIVO")
log.add_log("IMPORTA ARQUIVO")
escolhe_arquivo = bot.importar_layout(variaveis.arquivo_cetip, log)
print(f"{datetime.now()} - ARQUIVO IMPORTADO")
log.add_log("ARQUIVO IMPORTADO")