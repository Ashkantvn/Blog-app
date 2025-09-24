from django.shortcuts import render
from http import HTTPStatus

class CustomLoginRequiredMixin:
    permission_denied_template = ""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                self.permission_denied_template,
                context={"error": "You must be logged in to access this page."},
                status=HTTPStatus.UNAUTHORIZED
            )
        return super().dispatch(request, *args, **kwargs)
