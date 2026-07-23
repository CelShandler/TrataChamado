import pandas as pd
import os
from parser_descricao import processar_descricao, CAMPOS_EXTRAIR
from config import ARQUIVO_ENTRADA, ARQUIVO_SAIDA_FECHADOS, ARQUIVO_SAIDA_ATIVOS
from sqlite_manager import chamado_existe, registrar_lote_fechados
from utils import logger

def ler_planilha_entrada():
    if not os.path.exists(ARQUIVO_ENTRADA):
        logger.error(f"Arquivo não encontrado: {ARQUIVO_ENTRADA}")
        return None
    try:
        df = pd.read_excel(ARQUIVO_ENTRADA)
        return df
    except Exception as e:
        logger.error(f"Erro ao ler a planilha: {e}")
        return None

def processar_df(df):
    fechados_para_adicionar = []
    ativos_para_adicionar = []
    
    # Excluir colunas indesejadas
    colunas_remover = ["Inquilino", "Cidade_Cliente", "Endereço_Cliente"]
    df = df.drop(columns=[c for c in colunas_remover if c in df.columns], errors='ignore')
    
    # Renomear e processar colunas
    rename_dict = {}
    for c in df.columns:
        if str(c).lower() == "estado":
            rename_dict[c] = "Status"
        elif str(c).lower() == "descrição" or str(c).lower() == "descricao":
            rename_dict[c] = "Descricao_Detalhada"
    df = df.rename(columns=rename_dict)
    
    # Mapear Status
    if "Status" in df.columns:
        status_map = {
            "Open": "Aberto",
            "Resolved": "Resolvido",
            "Suspended": "Suspenso",
            "Transfer": "Transferido",
            "Closed": "Fechado",
            "open": "Aberto",
            "resolved": "Resolvido",
            "suspended": "Suspenso",
            "transfer": "Transferido",
            "closed": "Fechado"
        }
        df["Status"] = df["Status"].replace(status_map)
        
    numeros_fechados = []
    
    total_lidos = len(df)
    ja_existiam = 0
    processados = 0
    erros = 0
    
    for index, row in df.iterrows():
        try:
            cols = df.columns
            # Normalizar os nomes p/ facilitar a busca:
            cols_lower = [str(c).lower() for c in cols]
            
            # Buscar nome real das colunas 
            col_numero = cols[cols_lower.index('número')] if 'número' in cols_lower else cols[cols_lower.index('numero')] if 'numero' in cols_lower else None
            if not col_numero:
                col_numero = cols[0]
                
            col_estado = 'Status' if 'Status' in cols else (cols[cols_lower.index('status')] if 'status' in cols_lower else None)
            col_metodo = 'Metodo Relatado' if 'Metodo Relatado' in cols else (cols[cols_lower.index('metodo relatado')] if 'metodo relatado' in cols_lower else 'Método Relatado')
            if col_metodo not in cols:
                col_metodo = cols[cols_lower.index('método relatado')] if 'método relatado' in cols_lower else None
                
            col_descricao = 'Descricao_Detalhada' if 'Descricao_Detalhada' in cols else (cols[cols_lower.index('descricao_detalhada')] if 'descricao_detalhada' in cols_lower else None)
            col_localidade = 'Localidade' if 'Localidade' in cols else (cols[cols_lower.index('localidade')] if 'localidade' in cols_lower else None)
            
            numero = row.get(col_numero)
            estado = str(row.get(col_estado, "")).strip().lower() if col_estado else ""
            metodo = str(row.get(col_metodo, "")) if col_metodo else ""
            descricao = str(row.get(col_descricao, "")) if col_descricao else ""
            localidade = str(row.get(col_localidade, "")) if col_localidade else ""
            
            is_closed = estado in ["closed", "fechado"]
            
            if is_closed:
                if chamado_existe(numero):
                    ja_existiam += 1
                    continue # Ignora, já está no banco e na planilha
            
            # Extração
            dados_extraidos = processar_descricao(descricao, metodo, localidade)
            
            # Montar a nova linha
            nova_linha = row.to_dict()
            nova_linha.update(dados_extraidos)
            
            if is_closed:
                fechados_para_adicionar.append(nova_linha)
                numeros_fechados.append(numero)
            else:
                ativos_para_adicionar.append(nova_linha)
                
            processados += 1
            
        except Exception as e:
            logger.error(f"Erro processando linha {index} (Chamado {row.get(col_numero, 'Desconhecido')}): {e}")
            erros += 1

    # Salvando os fechados
    if fechados_para_adicionar:
        df_novos_fechados = pd.DataFrame(fechados_para_adicionar)
        if os.path.exists(ARQUIVO_SAIDA_FECHADOS):
            df_fechados_antigos = pd.read_excel(ARQUIVO_SAIDA_FECHADOS)
            df_fechados_final = pd.concat([df_fechados_antigos, df_novos_fechados], ignore_index=True)
            df_fechados_final.to_excel(ARQUIVO_SAIDA_FECHADOS, index=False)
        else:
            df_novos_fechados.to_excel(ARQUIVO_SAIDA_FECHADOS, index=False)
            
        # Atualiza o DB
        registrar_lote_fechados(numeros_fechados)

    # Salvando os ativos (sempre recriado)
    if ativos_para_adicionar:
        df_ativos = pd.DataFrame(ativos_para_adicionar)
        df_ativos.to_excel(ARQUIVO_SAIDA_ATIVOS, index=False)
        
    logger.info("=== Resumo do Processamento ===")
    logger.info(f"Total de linhas lidas: {total_lidos}")
    logger.info(f"Chamados Fechados já existentes no banco (ignorados): {ja_existiam}")
    logger.info(f"Chamados (Ativos + Novos Fechados) processados com sucesso: {processados}")
    logger.info(f"Erros de processamento: {erros}")
    logger.info(f"Novos Fechados salvos: {len(fechados_para_adicionar)}")
    logger.info(f"Ativos salvos (recriados): {len(ativos_para_adicionar)}")
