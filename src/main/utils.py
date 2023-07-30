from typing import Any



def context_handler(request, context:dict[str,Any]):
    print(request.session.get("phone"))
    context["customer_logged_in"] = request.session.get("phone")

    return context
