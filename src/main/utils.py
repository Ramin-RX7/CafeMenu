from typing import Any

from orders.forms import CustomerLoginForm


class EditableContexts:
    form_login_error = None


def reset_edited_context():
    attribute_names = [attr for attr in vars(EditableContexts).keys() if not attr.startswith('__')]
    for attr in attribute_names:
        setattr(EditableContexts,attr,None)


def context_handler(request):
    context = {}

    context["customer_logged_in"] = request.session.get("phone")

    context["login_form"] = CustomerLoginForm()

    attribute_names = [attr for attr in vars(EditableContexts).keys() if not attr.startswith('__')]
    for attr in attribute_names:
        context[attr] = getattr(EditableContexts, attr)

    reset_edited_context()

    return context
