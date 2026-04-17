# -*- coding: utf-8 -*-
"""
Script para gerar o relatório parcial em PDF.
Usa fpdf2 com fontes core + download de fontes free.
"""

from fpdf import FPDF
import re
import os

CAMINHO_MD = r"c:\Users\User\Documents\Univesp\antigravity\projeto-integrador-1\relatorio-parcial-qwen.md"
CAMINHO_PDF = r"c:\Users\User\Documents\Univesp\antigravity\projeto-integrador-1\relatorio-parcial-qwen.pdf"

# Carregar o Markdown
with open(CAMINHO_MD, "r", encoding="utf-8") as f:
    md_content = f.read()

# Substituir caracteres não suportados por latin-1
replacements = {
    "\u2014": "--",  # em-dash
    "\u2013": "-",   # en-dash
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote
    "\u201c": '"',   # left double quote
    "\u201d": '"',   # right double quote
    "\u2026": "...", # ellipsis
    "\u2022": "-",   # bullet
    "\u2500": "-",   # box drawings light horizontal
    "\u2502": "|",   # box drawings light vertical
    "\u251c": "+",   # box drawings light vertical and right
    "\u2514": "+",   # box drawings light up and right
    "\u252c": "+",   # box drawings light down and horizontal
    "\u250c": "+",   # box drawings light down and right
    "\u2518": "+",   # box drawings light up and left
    "\u2574": "-",   # box drawings light left
    "\u2575": "|",   # box drawings light up
    "\u2576": "-",   # box drawings light right
    "\u2577": "|",   # box drawings light down
    "\u2580": "=",   # upper half block
    "\u2584": "=",   # lower half block
    "\u2588": "=",   # full block
    "\u00e7": "c",   # c cedilla
    "\u00e1": "a",   # a acute
    "\u00e0": "a",   # a grave
    "\u00e3": "a",   # a tilde
    "\u00e9": "e",   # e acute
    "\u00e8": "e",   # e grave
    "\u00ed": "i",   # i acute
    "\u00f3": "o",   # o acute
    "\u00f5": "o",   # o tilde
    "\u00fa": "u",   # u acute
    "\u00fc": "u",   # u umlaut
    "\u00c7": "C",   # C cedilla
    "\u00c1": "A",   # A acute
    "\u00c0": "A",   # A grave
    "\u00c3": "A",   # A tilde
    "\u00c9": "E",   # E acute
    "\u00cd": "I",   # I acute
    "\u00d3": "O",   # O acute
    "\u00d5": "O",   # O tilde
    "\u00da": "U",   # U acute
    "\u00b0": "o",   # degree sign
    "\u00a7": "S",   # section sign
    "\u00a9": "(c)", # copyright
    "\u00ae": "(R)", # registered
    "\u2122": "(TM)",# trademark
}
for old, new in replacements.items():
    md_content = md_content.replace(old, new)

# Also remove any remaining non-latin-1 chars
import unicodedata
def strip_non_latin1(text):
    result = []
    for char in text:
        try:
            char.encode('latin-1')
            result.append(char)
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Replace with closest ascii approximation or space
            normalized = unicodedata.normalize('NFD', char)
            if len(normalized) > 1:
                # Try base character
                base = normalized[0]
                try:
                    base.encode('latin-1')
                    result.append(base)
                    continue
                except:
                    pass
            result.append('?')
    return ''.join(result)

md_content = strip_non_latin1(md_content)


class RelatorioPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.page_num_offset = 0

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, str(self.page_no() - self.page_num_offset), align="C")

    def chapter_title(self, text):
        self.set_font("helvetica", "B", 14)
        self.multi_cell(0, 8, text)
        self.ln(4)

    def section_title(self, text):
        self.set_font("helvetica", "B", 12)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def section_subtitle(self, text):
        self.set_font("helvetica", "I", 11)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def body_text(self, text):
        self.set_font("helvetica", "", 11)
        self.multi_cell(0, 6.5, text)
        self.ln(2)

    def bold_text(self, text):
        self.set_font("helvetica", "B", 11)
        self.multi_cell(0, 6.5, text)
        self.ln(2)

    def center_bold(self, text, size=14):
        self.set_font("helvetica", "B", size)
        w = self.get_string_width(text) + 6
        self.set_x((self.w - w) / 2)
        self.cell(w, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def center_text(self, text, size=12):
        self.set_font("helvetica", "", size)
        w = self.get_string_width(text) + 6
        self.set_x((self.w - w) / 2)
        self.cell(w, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def code_block(self, text):
        self.set_font("courier", "", 8)
        self.set_fill_color(235, 235, 235)
        lines = text.split("\n")
        for line in lines:
            self.cell(0, 4.5, line[:95], fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def table_lines(self, lines):
        self.set_font("helvetica", "", 9)
        for line in lines:
            # Truncate very long lines to avoid layout issues
            if len(line) > 150:
                line = line[:150] + "..."
            try:
                self.multi_cell(0, 5.5, line)
            except Exception:
                # Fallback: just print as cell
                self.cell(0, 5.5, line[:90], new_x="LMARGIN", new_y="NEXT")
        self.ln(2)


pdf = RelatorioPDF()

# ===== CAPA =====
pdf.add_page()
pdf.ln(40)
pdf.center_text("UNIVERSIDADE VIRTUAL DO ESTADO DE SAO PAULO", 14)
pdf.ln(20)
pdf.center_text("[Nome dos Integrantes]", 12)
pdf.ln(20)
pdf.center_bold("Desenvolvimento de um Software Web para Cadastro de", 13)
pdf.center_bold("Assistencia Social com Framework Flask,", 13)
pdf.center_bold("Banco de Dados Supabase e Controle de Versao Git", 13)
pdf.ln(20)
pdf.center_text("Cidade - SP", 12)
pdf.center_text("2026", 12)

# ===== FOLHA DE ROSTO =====
pdf.add_page()
pdf.ln(30)
pdf.center_text("UNIVERSIDADE VIRTUAL DO ESTADO DE SAO PAULO", 14)
pdf.ln(15)
pdf.center_text("[Nome dos Integrantes]", 12)
pdf.ln(20)
pdf.center_bold("Desenvolvimento de um Software Web para Cadastro de", 12)
pdf.center_bold("Assistencia Social com Framework Flask,", 12)
pdf.center_bold("Banco de Dados Supabase e Controle de Versao Git", 12)
pdf.ln(15)
pdf.set_font("helvetica", "", 11)
pdf.set_x(30)
pdf.multi_cell(pdf.w - 60, 6, "Relatorio Tecnico-Cientifico apresentado na disciplina de Projeto Integrador para o curso de Tecnologia em Informatica da Universidade Virtual do Estado de Sao Paulo (UNIVESP).", align="C")
pdf.ln(20)
pdf.center_text("Cidade - SP", 12)
pdf.center_text("2026", 12)

# ===== FICHA CATALOGRÁFICA =====
pdf.add_page()
pdf.set_font("helvetica", "", 11)
pdf.multi_cell(0, 6.5, "[Nome dos Integrantes]. Desenvolvimento de um Software Web para Cadastro de Assistencia Social com Framework Flask, Banco de Dados Supabase e Controle de Versao Git. 2026. Relatorio Tecnico-Cientifico. Tecnologia em Informatica - Universidade Virtual do Estado de Sao Paulo. Tutor: [Nome do Tutor]. Polo [Nome do Polo], 2026.")
pdf.ln(5)

# RESUMO
pdf.set_font("helvetica", "B", 12)
pdf.cell(0, 8, "RESUMO", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font("helvetica", "", 11)
pdf.multi_cell(0, 6.5, "Este relatorio apresenta o desenvolvimento de um sistema web para cadastro e gestao de beneficiarios da Assistencia Social, resultante da migracao de uma aplicacao desktop baseada em planilhas Excel para uma plataforma web acessivel via navegador. O sistema utiliza o framework Flask (Python) no backend, Bootstrap 5 no frontend e o Supabase (PostgreSQL 15) como banco de dados na nuvem. O projeto aplica na pratica conceitos de desenvolvimento web, banco de dados relacional e controle de versao com Git, proporcionando uma experiencia de aprendizagem baseada em projeto real. Os resultados parciais demonstram um sistema funcional com autenticacao de usuarios, CRUD completo de beneficiarios, gestao de composicao familiar, validacoes de documentos brasileiros (CPF, NIS/PIS) e integracao com API externa ViaCEP para busca de enderecos. O controle de versao foi praticado ao longo de todo o desenvolvimento, com historico de 7 commits registrados no repositorio Git.")
pdf.ln(3)
pdf.set_font("helvetica", "", 11)
pdf.multi_cell(0, 6.5, "PALAVRAS-CHAVE: Flask. Banco de Dados. Controle de Versao. Assistencia Social. Aplicacao Web. Git. PostgreSQL. Python.")

# ===== SUMÁRIO =====
pdf.add_page()
pdf.set_font("helvetica", "B", 12)
pdf.cell(0, 8, "SUMARIO", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
sumario_items = [
    ("1 INTRODUCAO", ""),
    ("2 DESENVOLVIMENTO", ""),
    ("    2.1 Objetivos", ""),
    ("    2.2 Justificativa e Delimitacao do Problema", ""),
    ("    2.3 Fundamentacao Teorica", ""),
    ("    2.4 Metodologia", ""),
    ("    2.5 Resultados Preliminares: Solucao Inicial", ""),
    ("REFERENCIAS", ""),
    ("APENDICE A - Estrutura do Banco de Dados (SQL)", ""),
    ("APENDICE B - Estrutura de Arquivos do Projeto", ""),
]
for item, _ in sumario_items:
    pdf.set_font("helvetica", "B" if not item.startswith("    ") else "", 11)
    pdf.cell(0, 7, item, new_x="LMARGIN", new_y="NEXT")

# ===== PROCESSAR O RESTANTE DO MARKDOWN =====
lines = md_content.split("\n")
i = 0
in_code_block = False
code_block_content = ""
in_table = False
table_lines = []
section_started = False

# Pular as linhas já cobertas (capa, rosto, sumário etc.)
skip_until = "# 1 INTRODU"

while i < len(lines):
    line = lines[i].rstrip()

    # Skip until introduction
    if skip_until and skip_until not in line:
        i += 1
        continue
    elif skip_until and skip_until in line:
        skip_until = None

    # Code blocks
    if line.startswith("```"):
        if in_code_block:
            pdf.code_block(code_block_content.strip())
            code_block_content = ""
            in_code_block = False
        else:
            in_code_block = True
        i += 1
        continue

    if in_code_block:
        code_block_content += line + "\n"
        i += 1
        continue

    # Skip --- separators
    if line.strip() == "---":
        i += 1
        continue

    # Skip HTML tags
    if line.strip().startswith("<") and line.strip().endswith(">"):
        i += 1
        continue

    # Headings
    if line.startswith("# "):
        text = re.sub(r'\[([^\]]+)\]', lambda m: m.group(1), line[2:].strip())
        text = text.replace("**", "")
        pdf.add_page()
        pdf.chapter_title(text)
        i += 1
        continue

    if line.startswith("## "):
        text = line[3:].strip().replace("**", "")
        pdf.section_title(text)
        i += 1
        continue

    if line.startswith("### "):
        text = line[4:].strip().replace("**", "")
        pdf.section_subtitle(text)
        i += 1
        continue

    if line.startswith("#### "):
        text = line[5:].strip().replace("**", "")
        pdf.section_subtitle(text)
        i += 1
        continue

    # Bold centered text (short lines)
    if line.startswith("**") and line.endswith("**") and len(line) < 80:
        text = line.strip().replace("**", "")
        pdf.set_font("helvetica", "B", 11)
        pdf.multi_cell(0, 6.5, text)
        pdf.ln(2)
        i += 1
        continue

    # Table rows (starting with |)
    if line.startswith("|"):
        if not in_table:
            in_table = True
            table_lines = []
        if "---" in line:
            i += 1
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        cells = [c.replace("**", "") for c in cells]
        table_lines.append(" | ".join(cells))
        i += 1
        continue
    elif in_table:
        pdf.table_lines(table_lines)
        in_table = False
        table_lines = []

    # Bullet points
    if line.strip().startswith("- "):
        text = line.strip()[2:].replace("**", "")
        text = re.sub(r'\[([^\]]+)\]', lambda m: m.group(1), text)
        text = re.sub(r'<[^>]+>', '', text)
        pdf.set_font("helvetica", "", 11)
        pdf.cell(5, 6.5, "* ")
        pdf.multi_cell(pdf.w - pdf.get_x() - pdf.r_margin - 10, 6.5, text)
        pdf.ln(1)
        i += 1
        continue

    # Empty lines
    if not line.strip():
        i += 1
        continue

    # Regular text
    text = line.strip()
    text = text.replace("**", "")
    text = re.sub(r'\[([^\]]+)\]\s*<([^>]+)>', r'\1. Disponivel em: <\2>.', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace("__( ", "(").replace(" )__", ")")

    if text:
        pdf.body_text(text)

    i += 1

# Salvar PDF
pdf.output(CAMINHO_PDF)
print(f"PDF gerado com sucesso: {CAMINHO_PDF}")
print(f"Tamanho do arquivo: {os.path.getsize(CAMINHO_PDF) / 1024:.1f} KB")
