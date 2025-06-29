from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# Create custom send mail view here.
class CustomSendMail(View):
    def send_mail(self, request, *args, **kwargs):
        protocol      = "https" if request.is_secure() else "http"
        domain        = request.get_host()
        message       = kwargs.get("message")
        template_name = kwargs.get("template_name")

        if template_name is None and message is None:
            raise Exception("Please provide a template name or message to send mail.")
        else:
            template_params = kwargs.get("template_params", {})
            template_params["protocol"] = protocol
            template_params["domain"] = domain
            html_message = render_to_string(template_name=template_name, context=template_params) if message is None else None

        subject        = kwargs.get("subject", f"{protocol}://{domain}")
        message        = strip_tags(kwargs.get("message"))
        from_email     = kwargs.get("from_email")
        recipient_list = kwargs.get("recipient_list")
        fail_silently  = kwargs.get("fail_silently", False)
        auth_user      = kwargs.get("auth_user", None)
        auth_password  = kwargs.get("auth_password", None)
        connection     = kwargs.get("connection", None)
        html_message   = html_message

        return send_mail(
            subject        = subject,
            message        = message,
            from_email     = from_email,
            recipient_list = recipient_list,
            fail_silently  = fail_silently,
            auth_user      = auth_user,
            auth_password  = auth_password,
            connection     = connection,
            html_message   = html_message,
        )