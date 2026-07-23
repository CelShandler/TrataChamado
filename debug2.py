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

def gerar_regex_padrao():
    escaped_campos = [re.escape(c) for c in CAMPOS_EXTRAIR]
    pattern_labels = r'(' + '|'.join(escaped_campos) + r')\s*:'
    return pattern_labels

PATTERN_LABELS = gerar_regex_padrao()
print("Pattern:", PATTERN_LABELS)

texto_descricao = "IP do Usuário: 172.19.205.17Categoria: GESIS | ADMINISTRATIVOS | Cadastro de usuário nos sistemasLogin: jose.aldenizioNome Completo: José Aldenízio Lima RegoTelefone: 68 99955 4256Ramal: 000Email: jose.aldenizio@tjac.jus.brLocalidade: Comarca de Rio Branco - Cidade da justiçaSetor: Cejusc/jetranPatrimônio: 0062668Local de Atuação: TJACNúmero de IP / ANYDESK: 000"

matches = list(re.finditer(PATTERN_LABELS, texto_descricao, re.IGNORECASE))
with open('debug2_regex.txt', 'w', encoding='utf-8') as f:
    f.write(f"Matches count: {len(matches)}\n")
    for m in matches:
        f.write(f"Match: {m.group(1)} at {m.start()} to {m.end()}\n")
    
    f.write("\nExtraction:\n")
    if matches:
        primeiro_match = matches[0]
        f.write(f"DescricaoNovo -> {texto_descricao[:primeiro_match.start()].strip()}\n")
    for i in range(len(matches)):
        atual = matches[i]
        label_raw = atual.group(1)
        start_val = atual.end()
        end_val = matches[i+1].start() if i + 1 < len(matches) else len(texto_descricao)
        valor = texto_descricao[start_val:end_val].strip()
        f.write(f"{label_raw} -> {valor}\n")
