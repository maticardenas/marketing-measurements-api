from datetime import date as datetime_date

from ninja import Schema
from ninja.errors import HttpError
from pydantic import (
    BaseModel,
    model_validator,
)


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

    @model_validator(mode="after")
    def end_date_should_be_greater_than_start_date(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise HttpError(
                status_code=400, message="End date should be greater than start date"
            )
        return self


class ChannelSalesPercentageSchema(Schema):
    channel: str
    percentage: str


class ChannelWeeklySalesSchema(Schema):
    channel: str
    year: int
    week: int
    sales: float
