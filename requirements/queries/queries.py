class ConfigQueries:
    def __init__(self):
        pass

    def query_sinqia(self):
        query = """
        SELECT 
            M.Carteira, 
            M.CdInstrFin AS CodigoIF, 
            Mc5.Nome AS NomeIF_Sinqia, 
            Mc5.CGC AS CNPJ,
			case 
			When Mc5auxiliar.TpRegmCndm = 0 then 'CFA'
			When Mc5auxiliar.TpRegmCndm = 1 then 'CFF'
			end as 'TipoIF'
        FROM (
            SELECT 
                VigInstrFinxCrt.Carteira, 
                InstrFin.CdInstrFin
            FROM 
                VigInstrFinxCrt
            LEFT JOIN 
                InstrFin ON InstrFin.Id = VigInstrFinxCrt.IdInstrFin
        ) AS M
        LEFT JOIN Mc5 ON Mc5.Carteira = M.Carteira
		LEFT JOIN MC5Auxiliar on Mc5auxiliar.Carteira = M.Carteira
        """
        return query

    def query_vxcotas(self, lista_cnpj, data):
        cnpj_string = ", ".join(f"'{cpf}'" for cpf in lista_cnpj)
        query = f"""
        SELECT DISTINCT ON (c."data", c."carteira")
            c."data" as "DataValor",
            c."cnpjFundo" as "CnpjFundo",
            c."nome" as "NomeIF_VxCotas",
            uh."valor" as "ValorCota"
        FROM cotas c
        JOIN (
            SELECT DISTINCT ON (h."idCotaOriginal")
                h."idCotaOriginal",
                h."valor",
                h."data",
                h."pl",
                h."quantidade"
            FROM historico h
            ORDER BY h."idCotaOriginal", h."data" DESC
        ) AS uh ON uh."idCotaOriginal" = c.id
        WHERE c."ultimoStatus" IN (3, 4, 5, 6, 7, 8, 9)
            AND c."data" = '{data}'
            AND c."cnpjFundo" IN ({cnpj_string})
        ORDER BY c."data" ASC, c."carteira" ASC;
        """
        return query