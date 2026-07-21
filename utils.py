import logging

def configurar_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("ExtracaoAranda")

logger = configurar_logger()

def limpar_texto(texto):
    """Remove espaços duplicados e converte NaN para string vazia"""
    if str(texto).lower() == 'nan' or texto is None:
        return ""
    # Remove espaços duplos
    texto_limpo = " ".join(str(texto).split())
    return texto_limpo
