from enum import Enum

CAMPAIGN_TYPES = [
    ("branding", "BRANDING"),
    ("performance", "PERFORMANCE"),
    ("always on", "ALWAYS ON"),
]

CHANNELS = [
    ("tv", "TV"),
    ("radio", "RADIO"),
    ("ooh", "OOH"),
    ("facebook", "FACEBOOK"),
    ("print", "PRINT"),
    ("tiktok", "TIKTOK"),
    ("instagram", "INSTAGRAM"),
    ("db360 - prospecting", "DB360"),
    ("db360 - retargeting", "DB360 - RETARGETING"),
    ("google - branded search", "GOOGLE - BRANDED SEARCH"),
    ("google - non-branded search", "GOOGLE - NON-BRANDED SEARCH"),
]


class ChannelsEnum(Enum):
    TV = "tv"
    RADIO = "radio"
    OOH = "ooh"
    FACEBOOK = "facebook"
    PRINT = "print"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    DB360_PROSPECTING = "db360 - prospecting"
    DB360_RETARGETING = "db360 - retargeting"
    GOOGLE_BRANDED_SEARCH = "google - branded search"
    GOOGLE_NON_BRANDED_SEARCH = "google - non-branded search"
