from datetime import datetime

from ninja import Schema
from pydantic import BaseModel


class MarketingDataSchema(BaseModel):
    product: str | None = None
    campaign_type: str | None = None
    channel: str | None = None
    date: datetime | None = None
    conversions: float | None = None


class MarketingDataFilterSchema(Schema):
    products: list[str] | None = None
    campaigns: list[str] | None = None
    campaign_types: list[str] | None = None
    channels: list[str] | None = None
