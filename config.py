import os

# Configurações de pastas e arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENTRADA_DIR = os.path.join(BASE_DIR, "entrada")
SAIDA_DIR = os.path.join(BASE_DIR, "saida")

ARQUIVO_ENTRADA = os.path.join(ENTRADA_DIR, "Aranda.xlsx")
ARQUIVO_SAIDA_FECHADOS = os.path.join(SAIDA_DIR, "Chamados_Fechados.xlsx")
ARQUIVO_SAIDA_ATIVOS = os.path.join(SAIDA_DIR, "Chamados_Ativos.xlsx")
DB_PATH = os.path.join(BASE_DIR, "chamadosF.db")

# Lista de Comarcas
COMARCAS = [
    "Rio Branco",
    "Porto Acre",
    "Porto Walter",
    "Jordão",
    "Santa Rosa",
    "Marechal Thaumaturgo",
    "Bujari",
    "Sena Madureira",
    "Manoel Urbano",
    "Feijó",
    "Tarauacá",
    "Cruzeiro do Sul",
    "Mâncio Lima",
    "Rodrigues Alves",
    "Senador Guiomard",
    "Capixaba",
    "Acrelândia",
    "Plácido de Castro",
    "Xapuri",
    "Epitaciolândia",
    "Brasiléia",
    "Assis Brasil"
]

# Campos a serem extraídos da descrição
CAMPOS_EXTRAIR = [
    "Categoria",
    "Login",
    "Nome",
    "Telefone",
    "Ramal",
    "Email",
    "Comarca",
    "Setor",
    "Patrimônio",
    "Local de Atuação",
    "Número de IP / ANYDESK",
    "CPF",
    "Data de nascimento"
]
