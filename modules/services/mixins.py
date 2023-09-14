from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class AuthorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Необходимо авторизоваться!')
            return self.handle_no_permission()
        else:
            if not request.user.is_staff:
                if request.user != self.get_object().author:
                    messages.info(request, 'Изменение и удаление статьи доступно только автору')
                    return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    

class UserIsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True
    
    def handle_no_permission(self):
        return redirect('home')