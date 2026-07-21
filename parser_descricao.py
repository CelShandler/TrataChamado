import re
from config import COMARCAS, CAMPOS_EXTRAIR
from utils import limpar_texto

def extrair_comarca(localidade):
    localidade = str(localidade).strip()
    if not localidade or localidade.lower() == 'nan':
        return "Rio Branco"
    
    for comarca in COMARCAS:
        if comarca.lower() in localidade.lower():
            return comarca
    return "Rio Branco"

def gerar_regex_padrao():
    # Exemplo: (Categoria:|Login:|Nome:|...)
    # Para extrair tudo entre os marcadores
    escaped_campos = [re.escape(c) for c in CAMPOS_EXTRAIR]
    # Cria o padrão para buscar onde as labels começam
    pattern_labels = r'(' + '|'.join(escaped_campos) + r')\s*:'
    return pattern_labels

PATTERN_LABELS = gerar_regex_padrao()

def processar_descricao(texto_descricao, metodo_relatado, localidade):
    texto_descricao = str(texto_descricao)
    # Normalizar variações de labels comuns
    texto_descricao = re.sub(r'e-mail\s*:', 'Email:', texto_descricao, flags=re.IGNORECASE)
    texto_descricao = re.sub(r'localidade\s*:', 'Comarca:', texto_descricao, flags=re.IGNORECASE)
    texto_descricao = re.sub(r'localiza[çc][ãa]o\s*:', 'Comarca:', texto_descricao, flags=re.IGNORECASE)
    
    metodo_relatado = str(metodo_relatado)
    
    resultado = {campo: "" for campo in CAMPOS_EXTRAIR}
    resultado["DescricaoNovo"] = texto_descricao
    resultado["Comarca"] = extrair_comarca(localidade)
    
    # Validação do método relatado
    if "e-mail" in metodo_relatado.lower():
        # Retorna o dicionário vazio nos campos e a descrição original, conforme especificado
        return resultado
        
    # Usar regex para encontrar todas as posições dos marcadores
    # re.finditer retorna matches.
    matches = list(re.finditer(PATTERN_LABELS, texto_descricao, re.IGNORECASE))
    
    if not matches:
        return resultado
        
    # DescricaoNovo é o que vem antes do primeiro marcador
    primeiro_match = matches[0]
    resultado["DescricaoNovo"] = texto_descricao[:primeiro_match.start()].strip()
    
    # Processar cada campo encontrado
    for i in range(len(matches)):
        atual = matches[i]
        label_raw = atual.group(1) # Pode vir com caixa diferente (ex: categoria, LOGIN)
        
        # Encontrar o campo correto para atualizar no dicionário
        campo_correto = None
        for campo in CAMPOS_EXTRAIR:
            if campo.lower() == label_raw.lower():
                campo_correto = campo
                break
        
        if not campo_correto:
            continue
            
        start_val = atual.end()
        end_val = matches[i+1].start() if i + 1 < len(matches) else len(texto_descricao)
        
        valor = texto_descricao[start_val:end_val].strip()
        resultado[campo_correto] = limpar_texto(valor)
        
    # Limpa a string da comarca extraída pelo Regex mantendo apenas o nome padrão
    if resultado.get("Comarca"):
        resultado["Comarca"] = extrair_comarca(resultado["Comarca"])
        
    return resultado
