from pydantic import BaseModel, conint, validator
from typing import List, Literal


class Signatures(BaseModel):
    common: dict
    special: dict

    @validator('common', 'special')
    def validate_signatures(cls, v: dict):
        if not isinstance(v, dict):
            raise ValueError('must be a dictionary')
        if 'mobile' not in v or 'web' not in v:
            raise ValueError('must contain both "mobile" and "web" keys')
        if not isinstance(v['mobile'], int) or not isinstance(v['web'], int):
            raise ValueError('values for "mobile" and "web" must be integers')
        return v


class JsonData(BaseModel):
    clientId: str
    organizationId: str
    segment: Literal["Малый бизнес", "Средний бизнес", "Крупный бизнес"]
    role: Literal["ЕИО", "Сотрудник"]
    organizations: conint(ge=1, le=300)
    currentMethod: Literal["SMS", "PayControl", "КЭП на токене", "КЭП в приложени"]
    mobileApp: bool
    signatures: Signatures
    availableMethods: List[Literal["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"]]
    claims: conint(ge=0)


# Пример корректных данных:
example_json = {
    "clientId": "client081",
    "organizationId": "organization982",
    "segment": "Малый бизнес",
    "role": "Сотрудник",
    "organizations": 3,
    "currentMethod": "КЭП на токене",
    "mobileApp": True,
    "signatures": {
        "common": {
            "mobile": 3,
            "web": 10
        },
        "special": {
            "mobile": 5,
            "web": 6
        }
    },
    "availableMethods": ["SMS", "КЭП на токене"],
    "claims": 0
}
