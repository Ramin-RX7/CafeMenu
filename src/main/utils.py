from typing import Any



def context_handler(request):
    context = {}
    context["customer_logged_in"] = request.session.get("phone")

    return context
