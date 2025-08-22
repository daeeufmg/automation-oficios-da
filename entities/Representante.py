from dataclasses import dataclass, asdict
from typing import Dict

@dataclass
class Representante:
    nome: str = ""
    matricula: str = ""
    curso: str = ""
    email: str = ""
    email_ufmg: str = ""
    telefone: str = ""


    def preenchido(self) -> bool:
        """Retorna True se pelo menos um campo (além do curso) estiver preenchido."""
        campos_relevantes = [self.nome, self.matricula, self.email, self.email_ufmg, self.telefone]
        return any(c.strip() for c in campos_relevantes)
    
    def validar(self, tipo: str, cadeira_num: int):
        """Valida se todos os campos obrigatórios foram preenchidos."""
        if not self.nome.strip():
            raise ValueError(f"❌ Campo 'nome' ausente para o {tipo} da cadeira {cadeira_num}")
        if not self.matricula.strip():
            raise ValueError(f"❌ Campo 'matricula' ausente para o {tipo} da cadeira {cadeira_num}")
        if not self.email.strip():
            raise ValueError(f"❌ Campo 'email' ausente para o {tipo} da cadeira {cadeira_num}")
        if not self.email_ufmg.strip():
            raise ValueError(f"❌ Campo 'email_ufmg' ausente para o {tipo} da cadeira {cadeira_num}")
        if not self.telefone.strip():
            raise ValueError(f"❌ Campo 'telefone' ausente para o {tipo} da cadeira {cadeira_num}")

    def to_dict(self) -> Dict[str, str]:
        """Exporta para dict (ex: salvar em JSON)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        """Cria um Representante a partir de um dicionário (como no config.json)."""
        return cls(
            nome=data.get("nome", ""),
            matricula=data.get("matricula", ""),
            curso=data.get("curso", ""),
            email=data.get("email", ""),
            email_ufmg=data.get("email_ufmg", ""),
            telefone=data.get("telefone", "")
        )
