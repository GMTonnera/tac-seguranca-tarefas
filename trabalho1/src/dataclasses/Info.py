from dataclasses import dataclass

@dataclass
class Info:
    user_name: int 
    account_code: str 
    account_balance: int
    account_limit: int
    account_limit_used: int
    