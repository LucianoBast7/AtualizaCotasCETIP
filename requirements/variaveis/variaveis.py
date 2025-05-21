from dotenv import load_dotenv
import os
from datetime import datetime, date

# Configurando pasta
hoje = datetime.today()
data_atual = date.today()
ano = hoje.strftime("%Y")
mes = hoje.strftime("%m")
dia = hoje.strftime("%d")

pasta_arquivo = f"W:\\PY_018 - Atualiza Cotas CETIP\\97. Processa Arquivo\\{ano}\\{mes}\\{dia}"
os.makedirs(pasta_arquivo, exist_ok=True)
caminho_arquivo = os.path.join(pasta_arquivo, f"LayoutCetip.txt")

load_dotenv()

class ConfigVaraveies():
    def __init__(self):
        
        # Acessos Sinqia
        self.host_sinqia = os.getenv("HOST_SINQIA")
        self.database_sinqia = os.getenv("DATABASE_SINQIA")
        self.user_sinqia = os.getenv("USER_SINQIA")
        self.password_sinqia = os.getenv("PASSWORD_SINQIA")

        # Acessos VxCotas
        self.host_vxcotas = os.getenv("HOST_VXCOTAS")
        self.database_vxcotas = os.getenv("DATABASE_VXCOTAS")
        self.user_vxcotas = os.getenv("USER_VXCOTAS")
        self.password_vxcotas = os.getenv("PASSWORD_VXCOTAS")

        # Acessos Automate
        self.host_automate = os.getenv("HOST_AUTOMATE")
        self.database_automate = os.getenv("DATABASE_AUTOMATE")
        self.user_automate = os.getenv("USER_AUTOMATE")
        self.password_automate = os.getenv("PASSWORD_AUTOMATE")

        # Acessos Cetip
        self.empresa_cetip = os.getenv("PARTICIPANTE_CETIP")
        self.user_cetip = os.getenv("USER_CETIP")
        self.password_cetip = os.getenv("PASSWORD_CETIP")

        # Arquivo
        self.arquivo_cetip = caminho_arquivo