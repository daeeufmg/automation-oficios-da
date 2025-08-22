import json
from entities.Cadeira import Cadeira
from io import BytesIO
from assets.styles import *
from utils import *
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from datetime import datetime, date
from utils import set_pt_locale
from oficio_text import intro_text

def gerar_pdf(config):
    # Extrai dados principais
    oficio = config.get("oficio")
    data = formatar_data_ptbr(config.get("data"))

    orgao = config.get("orgao")
    tipo_orgao = config.get("tipo_orgao", "O").upper()
    presidente = config.get("presidente")
    contato_da = config.get("contato_da")
    contato_pres = config.get("contato_presidente")
    cadeiras: list[Cadeira] = get_cadeiras_from_dict(config)
    corpo_adicional = config.get("corpo_adicional", "")
    is_troca = config.get("is_troca", False)
    texto_troca = ""
    if is_troca:
        nomes = config.get("nomes_troca", "")
        texto_troca = f"Conforme os documentos de renúncia em anexo dos(as) membros(as) {nomes}, "

    # Define preposição conforme tipo
    preposicao = "na" if tipo_orgao == "A" else "no "
    assunto = f"Assunto: Nomeação de Representantes Discentes {preposicao} {orgao}"

    # Buffer para PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=3.65 * cm,
        rightMargin=2.35 * cm,
        topMargin=2.35 * cm,
        bottomMargin=2.5 * cm
    )
    
    content = intro_text(oficio=oficio,
                         data=data,
                         assunto=assunto,
                         texto_troca=texto_troca,
                         corpo_adicional=corpo_adicional, 
                         orgao=orgao)
    
    cadeiras = get_cadeiras_from_dict(config=config)
    for cadeira in cadeiras:
        if cadeira.validar():
            titular = cadeira.titular
            suplente = cadeira.suplente

            content.append(Paragraph(f"CADEIRA {cadeira.numero}:", bold))
            content.append(Paragraph(
                f"Titular: <b>{titular.nome}</b>, matrícula n.º {titular.matricula}, "
                f"estudante do {titular.curso}, e-mail: {titular.email}, "
                f"E-mail UFMG: {titular.email_ufmg}, telefone: {titular.telefone}",
                normal
            ))
            content.append(space(0.3))
            content.append(Paragraph(
                f"Suplente: <b>{suplente.nome}</b>, matrícula n.º {suplente.matricula}, "
                f"estudante do {suplente.curso}, e-mail: {suplente.email}, "
                f"E-mail UFMG: {suplente.email_ufmg}, telefone: {suplente.telefone}",
                normal
            ))
            content.append(space())
            content.append(space(0.5))


    content.extend([
        Paragraph("Solicitamos, por gentileza, que as ausências dos representantes discentes sejam\
        comunicadas ao DA EEUFMG para que possamos apoiar a participação estudantil\
        nos órgãos colegiados.\
        ", normal),
        space(0.5),
        Paragraph("Por fim, o Diretório Acadêmico da EE UFMG fica à disposição, sempre no melhor\
        interesse de representar os estudantes e contribuir para o desenvolvimento da Escola\
        de Engenharia e da UFMG.\
        ", normal),
        space(),
        Paragraph("Cordialmente,", normal),
        space(2),
        Paragraph("_______________________________", normal),
        Paragraph(presidente, bold),
        Paragraph(f"Contato do DA EEUFMG: {contato_da}", normal),
        Paragraph(f"Contato Presidente: {contato_pres}", normal),
    ])

    # Gera PDF
    doc.build(content)
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    set_pt_locale()
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    pdf_buffer = gerar_pdf(config)
    with open("saida_oficio.pdf", "wb") as out:
        out.write(pdf_buffer.read())
