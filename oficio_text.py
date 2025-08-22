from assets.styles import *
from reportlab.platypus import Image
from reportlab.platypus import Paragraph
from assets.styles import logo

def intro_text(oficio : str, data : str, assunto : str, texto_troca : str, corpo_adicional : str, orgao : str):
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
    return content