import os
from config import ENTRADA_DIR, SAIDA_DIR
from sqlite_manager import inicializar_banco
from excel_manager import ler_planilha_entrada, processar_df
from utils import logger

def verificar_pastas():
    if not os.path.exists(ENTRADA_DIR):
        os.makedirs(ENTRADA_DIR)
        logger.info(f"Pasta criada: {ENTRADA_DIR}")
    if not os.path.exists(SAIDA_DIR):
        os.makedirs(SAIDA_DIR)
        logger.info(f"Pasta criada: {SAIDA_DIR}")

def executar_pipeline():
    logger.info("Iniciando rotina de extração...")
    
    # 1. Pastas
    verificar_pastas()
    
    # 2. Inicializar banco
    logger.info("Inicializando/Verificando Banco de Dados...")
    inicializar_banco()
    
    # 3. Ler arquivo
    logger.info("Lendo planilha de entrada...")
    df = ler_planilha_entrada()
    
    if df is not None:
        logger.info("Processando dados...")
        processar_df(df)
        logger.info("Processamento finalizado com sucesso.")
    else:
        logger.warning("Pipeline abortada por falha na leitura do arquivo.")

if __name__ == "__main__":
    executar_pipeline()
