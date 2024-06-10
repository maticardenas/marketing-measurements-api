from core.models import APIToken


def generate_token(user: str) -> str:
    token, _ = APIToken.objects.get_or_create(user=user)
    return str(token.token)
