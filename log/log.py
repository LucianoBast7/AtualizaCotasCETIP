from datetime import datetime, date
import logging
import os

# Configurando Logs
hoje = datetime.today()
data_atual = date.today()
ano = hoje.strftime("%Y")
mes = hoje.strftime("%m")
dia = hoje.strftime("%d")

pasta_log = f"W:\\PY_018 - Atualiza Cotas CETIP\\0. Log\\{ano}\\{mes}\\{dia}"
os.makedirs(pasta_log, exist_ok=True)

caminho_log = os.path.join(pasta_log, f"AtualizaCotasCETIP_{data_atual}.log")

log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=caminho_log, filemode='a', level=logging.INFO, format=log_format)

class ConfigLog():
    def __init__(self):
        pass
    
    def add_log(self, msg: str, level: str = 'info'):
        if hasattr(logging, level):
            getattr(logging, level)(msg)
        else:
            logging.info(f"[Nível inválido: {level}] {msg}")