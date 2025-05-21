from datetime import datetime
import pandas as pd
import sys


class ConfigLayout():
    def __init__(self):
        pass

    def criar_layout(self, dataframe, mensagem, arquivo, lgr):
        try:
            if mensagem == "SEM DADOS PARA PROCESSAR":
                vazio = ""
                with open(arquivo, "w", encoding="utf-8") as file:
                    file.write(vazio)
            else:
                # Header
                tipoif_header = "CFF".ljust(5)
                tiporegistro_header = "0"
                acao_header = "LCOP"
                nomeempresa_header = "123456789".ljust(20)
                data_hoje = datetime.now().strftime("%Y%m%d")
                versaolayout_header = "00006"
                delimitador_header = "<"

                header = f"{tipoif_header}{tiporegistro_header}{acao_header}{nomeempresa_header}{data_hoje}{versaolayout_header}{delimitador_header}"

                # Linhas de Registro
                dataframe["DataValor"] = pd.to_datetime(dataframe["DataValor"]).dt.strftime("%Y%m%d")
                # dataframe["ValorCota"] = dataframe["ValorCota"].apply(lambda x: f"{x:0>20.6f}".replace(".", ","))
                dataframe["ValorCota"] = dataframe["ValorCota"].astype(float).apply(
                    lambda x: f"{int(x):012d},{str(f'{x:.8f}').split('.')[1]}"
                )



                linhas = []
                for _, row in dataframe.iterrows():
                    linha = (
                        row["TipoIF"].ljust(5) +
                        "1" +
                        "0015" +
                        row["CodigoIF"].ljust(14) +
                        " " * (490 - 25) + 
                        row["DataValor"] +
                        row["ValorCota"]
                    )
                    linhas.append(linha)
                
                conteudo = '\n'.join([header] + linhas)

                with open(arquivo, "w", encoding="utf-8") as file:
                    file.write(conteudo)
        except Exception as e:
            lgr.add_log(f"ERRO AO CRIAR LAYOUT CETIP: {e}", level='error')

