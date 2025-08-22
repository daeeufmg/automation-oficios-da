from dataclasses import dataclass
from typing import Dict
from entities.Representante import Representante  # assumindo que está em outro arquivo

@dataclass
class Cadeira:
    titular: Representante
    suplente: Representante
    numero: int  # número da cadeira

    def validar(self):
        if self.titular.preenchido():
            self.titular.validar("titular", self.numero)
        else:
            return False
        
        if self.suplente.preenchido():
            self.suplente.validar("suplente", self.numero)
        else:
            return False
        
        return True
    
    def to_dict(self) -> Dict:
        """Exporta a cadeira para dict (JSON serializável)."""
        return {
            "numero": self.numero,
            "titular": self.titular.to_dict(),
            "suplente": self.suplente.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Cria uma cadeira a partir de dict (como no config.json)."""
        titular = Representante.from_dict(data.get("titular", {}))
        suplente = Representante.from_dict(data.get("suplente", {}))
        numero = data.get("numero", 0)  # caso não exista, atribui 0
        return cls(titular=titular, suplente=suplente, numero=numero)
