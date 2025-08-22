from reportlab.lib import utils
import locale
from typing import Any
from entities.Cadeira import Cadeira
from reportlab.platypus import Image
from reportlab.lib.units import cm
from typing import List
from datetime import datetime, date

def set_pt_locale():
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR')  # alternativa para Windows
        except locale.Error:
            print("⚠️ Locale pt_BR não está disponível no sistema. Os meses podem aparecer em inglês.")

def formatar_data_ptbr(data) -> str:
    if isinstance(data, (datetime, date)):
        return data.strftime("%d de %B de %Y")
    elif isinstance(data, str):
        try:
            dt = datetime.strptime(data, "%Y-%m-%d")
            return dt.strftime("%d de %B de %Y")
        except ValueError:
            raise ValueError(f"Formato de string de data inválido: {data}")
    else:
        raise ValueError(f"Formato de data inválido: {type(data)}")

def get_cadeiras_from_dict(config: dict[str, Any]) -> List[Cadeira]:
    cadeiras = []
    cadeiras_json = config.get("cadeiras", [])
    for idx, cadeira_data in enumerate(cadeiras_json, start=1):
        cadeira = Cadeira.from_dict(cadeira_data)
        cadeira.numero = idx
        cadeiras.append(cadeira)
    return cadeiras

def get_image(path, width=5*cm) -> Image:
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect), hAlign='CENTER')
