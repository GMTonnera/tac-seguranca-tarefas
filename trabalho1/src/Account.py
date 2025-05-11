from dataclasses import dataclass

@dataclass
class Account:
    id: int | None
    fk_user_id: str 
    cd_account: str | None
    vr_account_balance: int
    vr_account_limit: int
    vr_account_limit_used: int
