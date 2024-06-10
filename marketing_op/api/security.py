from django.http import HttpRequest
from ninja.security import HttpBasicAuth, HttpBearer

from core.models import APIToken


class BasicAuth(HttpBasicAuth):
    def authenticate(
        self, request: HttpRequest, username: str, password: str
    ) -> str | None:
        if username == "marketing_op" and password == "marketing_op_supersecret":
            return username


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if APIToken.objects.filter(token=token).exists():
            return token
        return None
