import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Image
from reportlab.lib import utils
from reportlab.lib.enums import TA_JUSTIFY
from datetime import datetime, date
import locale

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR')  # alternativa para Windows
    except locale.Error:
        print("⚠️ Locale pt_BR não está disponível no sistema. Os meses podem aparecer em inglês.")

def validar_representante(tipo, dados, cadeira_num):
    campos_obrigatorios = ["nome", "matricula", "curso", "email", "email_ufmg", "telefone"]
    for campo in campos_obrigatorios:
        if campo not in dados or not dados[campo]:
            raise ValueError(f"❌ Campo obrigatório ausente para o {tipo} da cadeira {cadeira_num}: '{campo}'")



def get_image(path, width=5*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect), hAlign='CENTER')



def gerar_pdf(config):
    # Extrai dados principais
    oficio = config.get("oficio")
    data = config.get("data")

    if isinstance(data, (datetime, date)):
        data = data.strftime("%d de %B de %Y")
    elif isinstance(data, str):
        try:
            data = datetime.strptime(data, "%Y-%m-%d").strftime("%d de %B de %Y")
        except ValueError:
            pass
    else:
        raise ValueError("Formato de data inválido.")

    orgao = config.get("orgao")
    tipo_orgao = config.get("tipo_orgao", "O").upper()
    presidente = config.get("presidente")
    contato_da = config.get("contato_da")
    contato_pres = config.get("contato_presidente")
    cadeiras = config.get("cadeiras", [])
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
        topMargin=2.35 * cm,  # mesmo topo em todas as páginas
        bottomMargin=2.5 * cm
    )

    # Estilos
    styles = getSampleStyleSheet()

    normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY
    )

    bold = ParagraphStyle(
        'bold',
        parent=normal,
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY
    )

    center_small = ParagraphStyle(
        'center_small',
        parent=normal,
        fontName='Times-Bold',
        alignment=1,
        fontSize=10,
        leading=16,
    )

    right = ParagraphStyle(
        'right',
        parent=normal,
        alignment=2,
        leading=16,
    )

    space = lambda h=0.4: Spacer(1, h * cm)
    body_spacing = 0.3

    logo = get_image("logo_da.png", width=9*cm)

    content = [
        space(-2.1),
        logo,
        space(.2),
        Paragraph("UNIVERSIDADE FEDERAL DE MINAS GERAIS", center_small),
        Paragraph("ESCOLA DE ENGENHARIA", center_small),
        Paragraph("DIRETÓRIO ACADÊMICO", center_small),
        space(0.5),
        Paragraph(f"OFÍCIO N.º {oficio}/DAEE", bold),
        Paragraph(f"Belo Horizonte, {data}.", right),
        space(0.4),
        Paragraph("Aos Srs.", normal),
        Paragraph("Professor Cícero Murta Starling", bold),
        Paragraph("Diretor da Escola de Engenharia da UFMG", normal),
        space(0.6),
        Paragraph("Professor Henrique Resende Martins", bold),
        Paragraph("Vice-Diretor da Escola de Engenharia da UFMG", normal),
        space(0.8),
        Paragraph(f"{assunto}", bold),
        space(body_spacing+0.2),
        Paragraph("Prezados Senhores Diretores,", normal),
        space(body_spacing),
        Paragraph("CONSIDERANDO os artigos 78, 79, 80 e 84 do Estatuto da UFMG,", normal),
        space(body_spacing),
        Paragraph("CONSIDERANDO os artigos 95, 100, 101 e 102 do Regimento Geral da UFMG,", normal),
        space(body_spacing),
        Paragraph("CONSIDERANDO o Estatuto Social do Diretório Acadêmico da Escola de\
        Engenharia da UFMG e sendo esse reconhecido como entidade de representação\
        discente no âmbito da EEUFMG, com ata de eleição e posse de seus dirigentes\
        devidamente cientificada ao Diretor da Unidade,\
        ", normal),
        space(body_spacing),
        Paragraph(f"{texto_troca}O DA EEUFMG indica e solicita a nomeação, a partir da presente data e com\
        mandato de 1 ano ou até o registro de nova ata de eleição e posse comunicada ao\
        Diretor, dos discentes abaixo listados como representantes discentes para composição\
        do órgão colegiado citado.", normal),

        Paragraph(corpo_adicional, normal),
        space(),
        Paragraph(f"Órgão Colegiado: {orgao}", bold),
        space(),
    ]

    # Itera sobre cada cadeira
    for idx, cadeira in enumerate(cadeiras, start=1):
        if not cadeira:
            continue

        titular = cadeira.get("titular", {})
        suplente = cadeira.get("suplente", {})

        validar_representante("titular", titular, idx)
        validar_representante("suplente", suplente, idx)

        content.append(Paragraph(f"CADEIRA {idx}:", bold))
        content.append(Paragraph(
            f"Titular: <b>{titular['nome']}</b>, matrícula n.º {titular['matricula']}, "
            f"estudante do {titular['curso']}, e-mail: {titular['email']}, "
            f"E-mail UFMG: {titular['email_ufmg']}, telefone: {titular['telefone']}",
            normal
        ))
        content.append(space(0.3))
        content.append(Paragraph(
            f"Suplente: <b>{suplente['nome']}</b>, matrícula n.º {suplente['matricula']}, "
            f"estudante do {suplente['curso']}, e-mail: {suplente['email']}, "
            f"E-mail UFMG: {suplente['email_ufmg']}, telefone: {suplente['telefone']}",
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
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    pdf_buffer = gerar_pdf(config)
    with open("saida_oficio.pdf", "wb") as out:
        out.write(pdf_buffer.read())
