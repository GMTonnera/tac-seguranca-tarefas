from dataclasses import dataclass

@dataclass
class User:
    id: int | None
    fk_account_id: int
    name: str
    password: str | None
