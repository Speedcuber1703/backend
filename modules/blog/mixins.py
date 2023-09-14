from .models import ViewCount
from modules.services.utils import get_client_ip


class ViewCountMixin:
    """
    Миксин для увеличения счётчика просмотра статьи
    """

    def get_object(self):
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        ViewCount.objects.get_or_create(article=obj, ip_address=ip_address)
        return obj