import pandas as pd
import pyodbc
import numpy as np
from sqlalchemy import create_engine, text
import re

class ConfigSQL():
    def __init__(self):
        pass

    def connection_string(self, server, database, user, password):
        # Connection String
        connection = f"DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password};Encrypt=no"
        conn = pyodbc.connect(connection)
        return conn

    def executa_query(self, consulta, host, database, user, password, lgr):
        try:
            conn = self.connection_string(host, database, user, password)
            df = pd.read_sql(consulta, conn, dtype={"CNPJ": str})
            conn.close()
            return df
        except Exception as e:
            lgr.add_log(f"ERRO AO CAPTURAR DADOS: {e}", level='error')
            
    def formatar_cnpj(self, cnpj):
        cnpj_num = int(float(cnpj))
        cnpj_str = str(cnpj_num).zfill(14)
        return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:]}"

    def lista_cnpj(self, dataframe, lgr):
        try:
            df = (
                dataframe["CNPJ"]
                .dropna()
                .apply(lambda x: self.formatar_cnpj(x))
                .tolist()
            )
            return df
        except Exception as e:
            lgr.add_log(f"ERRO AO CRIAR LISTA CNPJ: {e}", level='error')

    def executa_query_vxcotas(self, consulta, host, database, user, password, lgr):
        try:
            engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")
            with engine.connect() as connection:
                df = pd.read_sql(text(consulta), con=connection)
                df["ValorCota"] = df["ValorCota"].round(8)
                df["ValorCota"] = df["ValorCota"].apply(lambda x: f"{x:.8f}")
            return df
        except Exception as e:
            lgr.add_log(f"ERRO AO CAPTURAR DADOS: {e}", level='error')
    
    def casa_dados(self, dataframe1, dataframe2, lgr):
        try:
                dataframe1["NomeIF_VxCotas"] = (
                    dataframe1["NomeIF_VxCotas"]
                    .astype(str)                           # garante que tudo é string
                    .str.strip()                           # remove espaços no início e no fim
                    .str.replace(r"\s+", " ", regex=True)  # substitui múltiplos espaços por apenas um
                )
                dataframe2["NomeIF_Sinqia"] = (
                    dataframe2["NomeIF_Sinqia"]
                    .astype(str)
                    .str.strip()
                    .str.replace(r"\s+", " ", regex=True)
                )            
                
                DataframeFinal = pd.merge(
                    dataframe1,
                    dataframe2,
                    how="outer",
                    left_on="NomeIF_VxCotas",
                    right_on="NomeIF_Sinqia"
                )

                DataframeFinal["DiferencaNome"] = DataframeFinal.apply(
                        lambda row: "CORRETO" if row["NomeIF_VxCotas"] == row["NomeIF_Sinqia"] else "INCORRETO",
                        axis=1
                    )
                
                DataframeFinal = DataframeFinal[DataframeFinal["DiferencaNome"] == "CORRETO"]

                DataframeFinal = DataframeFinal[[
                    "TipoIF",
                    "CodigoIF",
                    "DataValor",
                    "ValorCota",
                    "CnpjFundo"
                ]]
                DataframeFinal = DataframeFinal.drop_duplicates(subset=["ValorCota", "CnpjFundo"], keep="first")
                #DataframeFinal = DataframeFinal[DataframeFinal["CodigoIF"] == "4354924SEN"]
                return DataframeFinal
        except Exception as e:
            lgr.add_log(f"ERRO AO CASAR DADOS: {e}", level='error')

    def registros_atualizados(self, dataframe, host, database, user, password, lgr):
        try:
            query = """
            SELECT 
                CodigoIF, 
                DataValor, 
                ValorCota, 
                CnpjFundo
            FROM dbo.tbProcessPY018
            """

            engine = self.connection_string(host, database, user, password)
            df_base_processamento = pd.read_sql(query, con=engine)
            
            if not df_base_processamento.empty:
                df_base_processamento["DataValor"] = df_base_processamento["DataValor"].dt.strftime("%Y-%m-%d")
                dataframe["DataValor"] = pd.to_datetime(dataframe["DataValor"]).dt.strftime("%Y-%m-%d")

                dataframe["ValorCota"] = dataframe["ValorCota"].astype(float)
                df_base_processamento["ValorCota"] = df_base_processamento["ValorCota"].astype(float)

                # Merge com Dados Casados
                df_base_processamento = df_base_processamento.rename(columns={
                    "CodigoIF": "CodigoIF_Prs",
                    "DataValor": "DataValor_Prs",
                    "ValorCota": "ValorCota_Prs",
                    "CnpjFundo": "CnpjFundo_Prs"
                })

                DataframeFinal = pd.merge(
                    dataframe,
                    df_base_processamento,
                    how="outer",
                    left_on=["CodigoIF", "DataValor", "ValorCota", "CnpjFundo"],
                    right_on=["CodigoIF_Prs", "DataValor_Prs", "ValorCota_Prs", "CnpjFundo_Prs"]
                )

                DataframeFinal["Filtro"] = DataframeFinal.apply(
                        lambda row: "PROCESSADO" if row["CodigoIF"] == row["CodigoIF_Prs"] 
                        and row["DataValor"] == row["DataValor_Prs"] 
                        and row["ValorCota"] == row["ValorCota_Prs"] 
                        and row["CnpjFundo"] == row["CnpjFundo_Prs"] else "NAO PROCESSADO",
                        axis=1
                    )
                
                DataframeFinal = DataframeFinal[DataframeFinal["Filtro"] == "NAO PROCESSADO"]
                DataframeFinal = DataframeFinal[[
                    "TipoIF",
                    "CodigoIF",
                    "DataValor",
                    "ValorCota",
                    "CnpjFundo"
                ]]
                DataframeFinal = DataframeFinal.dropna(how='all')
                return DataframeFinal
            else:
                return dataframe
        except Exception as e:
            lgr.add_log(f"ERRO AO FILTRAR DADOS: {e}")

    def envia_processamento(self, dataframe, host, database, user, password, lgr):
        try:
            if not dataframe.empty:
                dados = dataframe[["TipoIF", "CodigoIF", "DataValor", "ValorCota", "CnpjFundo"]].values.tolist()
                conn = self.connection_string(host, database, user, password)
                cursor = conn.cursor()

                query = """
                    INSERT INTO dbo.tbProcessPY018 (
                        TipoIF, CodigoIF, DataValor, ValorCota, CnpjFundo, DataProcessamento
                    ) VALUES (?, ?, ?, ?, ?, GETDATE())
                """

                cursor.executemany(query, dados)

                conn.commit()
                cursor.close()
                conn.close()
                result = "BASE PROCESSAMENTO ATUALIZADA"
                return result
            else:
                result = "SEM DADOS PARA PROCESSAR"
                return result
        except Exception as e:
            lgr.add_log(f"ERRO AO SALVAR DADOS NO BANCO: {e}", level='error')

    def limpa_fundo(self, fundo, host, database, user, password, lgr):
        try:
            if fundo != "":
                query = f"""
                    UPDATE dbo.tb_ConfigRobos
                    SET VALOR_PARAMETRO = ''
                    WHERE id LIKE '2186';
                """

                conn = self.connection_string(host, database, user, password)
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
                result = "VARIAVEL FUNDO LIMPA"
                return result
            else:
                result = "SEM FUNDO PARA LIMPAR"
                return result
        except Exception as e:
            lgr.add_log(f"ERRO AO LIMPAR VARIAVEL: {e}")
            
    
            