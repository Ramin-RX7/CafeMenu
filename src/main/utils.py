from orders.forms import CustomerLoginForm
from users.models import User

class EditableContexts:
    form_login_error = None


def reset_edited_context():
    attribute_names = [attr for attr in vars(EditableContexts).keys() if not attr.startswith('__')]
    for attr in attribute_names:
        setattr(EditableContexts,attr,None)


def dynamic_menu_context():
    from dynamic_menu.models import MainInfo,Social
    context = {
        "maininfo": MainInfo.objects.all().first(),
        "socials": Social.objects.all().first(),
    }
    try:
        social_instance = Social.objects.all().first()
        context["socials"] = {field.name:getattr(social_instance, field.name) for field in social_instance._meta.fields[3:] if getattr(social_instance, field.name)}
    except:
        context["socials"] = {}

    return context




def context_handler(request):
    context = {}

    context["logged_in"] = request.session.get("phone") or isinstance(request.user, User)

    context["login_form"] = CustomerLoginForm()


    attribute_names = [attr for attr in vars(EditableContexts).keys() if not attr.startswith('__')]
    for attr in attribute_names:
        context[attr] = getattr(EditableContexts, attr)

    reset_edited_context()


    context.update(dynamic_menu_context())

    return context
