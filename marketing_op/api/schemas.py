from datetime import date as datetime_date

from ninja import Schema
from pydantic import BaseModel


class MarketingDataSchema(BaseModel):
    product: str | None = None
    campaign_type: str | None = None
    campaign: str | None = None
    channel: str | None = None
    date: datetime_date | None = None
    conversions: float | None = None


class MarketingDataFilterSchema(Schema):
    products: list[str] | None = None
    campaigns: list[str] | None = None
    campaign_types: list[str] | None = None
    channels: list[str] | None = None
    start_date: datetime_date | None = None
    end_date: datetime_date | None = None


class ChannelSalesPercentageSchema(Schema):
    channel: str
    percentage: str


class ChannelWeeklySalesSchema(Schema):
    channel: str
    year: int
    week: int
    sales: float
