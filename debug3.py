import re

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

def extrair_comarca(localidade):
    return "Rio Branco"

def gerar_regex_padrao():
    escaped_campos = [re.escape(c) for c in CAMPOS_EXTRAIR]
    pattern_labels = r'(' + '|'.join(escaped_campos) + r')\s*:'
    return pattern_labels

PATTERN_LABELS = gerar_regex_padrao()

def processar_descricao(texto_descricao, metodo_relatado, localidade):
    texto_descricao = str(texto_descricao)
    texto_descricao = re.sub(r'e-mail\s*:', 'Email:', texto_descricao, flags=re.IGNORECASE)
    texto_descricao = re.sub(r'localidade\s*:', 'Comarca:', texto_descricao, flags=re.IGNORECASE)
    texto_descricao = re.sub(r'localiza[çc][ãa]o\s*:', 'Comarca:', texto_descricao, flags=re.IGNORECASE)
    
    resultado = {campo: "" for campo in CAMPOS_EXTRAIR}
    resultado["DescricaoNovo"] = texto_descricao
    resultado["Comarca"] = extrair_comarca(localidade)
    
    matches = list(re.finditer(PATTERN_LABELS, texto_descricao, re.IGNORECASE))
    
    if not matches:
        return resultado
        
    primeiro_match = matches[0]
    resultado["DescricaoNovo"] = texto_descricao[:primeiro_match.start()].strip()
    
    for i in range(len(matches)):
        atual = matches[i]
        label_raw = atual.group(1)
        
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
        resultado[campo_correto] = valor
        
    return resultado

texto = "IP do Usuário: 172.19.205.17Categoria: GESIS | ADMINISTRATIVOS | Cadastro de usuário nos sistemasLogin: jose.aldenizioNome Completo: José Aldenízio Lima RegoTelefone: 68 99955 4256Ramal: 000Email: jose.aldenizio@tjac.jus.brLocalidade: Comarca de Rio Branco - Cidade da justiçaSetor: Cejusc/jetranPatrimônio: 0062668Local de Atuação: TJACNúmero de IP / ANYDESK: 000"

res = processar_descricao(texto, "", "")
with open('debug3_out.txt', 'w', encoding='utf-8') as f:
    for k, v in res.items():
        f.write(f"{k} -> {v}\n")
