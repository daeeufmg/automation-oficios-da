from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Spacer
from reportlab.lib.enums import TA_JUSTIFY
from utils import get_image
import os

body_spacing = 0.3
logo = get_image(os.path.join("assets","logo_da.png"), width=9*cm)

# Estilos
styles = getSampleStyleSheet()
space = lambda h=0.4: Spacer(1, h * cm)
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