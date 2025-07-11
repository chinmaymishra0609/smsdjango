from django.shortcuts import render

# Import Django's base class-based view (CBV) which provides structure for GET, POST, etc.
from django.views import View

# Import Django's built-in function to send emails.
# This handles composing and delivering plain text and HTML emails.
from django.core.mail import send_mail

# Import utility to remove HTML tags from a string.
# Commonly used to extract plain text from HTML content.
from django.utils.html import strip_tags

# Import utility to render a Django template into a string.
# Useful when sending HTML emails or preparing dynamic content.
from django.template.loader import render_to_string

# Create custom send mail view here.
class CustomSendMail(View):
    def send_mail(self, request, *args, **kwargs):
        """
        Send an email using either a plain text message or a rendered HTML template.

        This method supports both static messages and dynamic templates. It adds the current
        request's protocol and domain to the template context if provided.

        Args:
            request (HttpRequest): The current HTTP request object.
            *args: Additional positional arguments (not used).
            **kwargs: Keyword arguments for mail configuration, including:
                - message (str): Plain text message to send (optional if template is provided).
                - template_name (str): Template path to render as email body (optional if message is provided).
                - template_params (dict): Context to pass into the template.
                - subject (str): Subject of the email. Defaults to protocol://domain.
                - from_email (str): Sender's email address.
                - recipient_list (list): List of recipients.
                - fail_silently (bool): Whether to suppress exceptions. Default is False.
                - auth_user (str): Username for SMTP authentication.
                - auth_password (str): Password for SMTP authentication.
                - connection (EmailBackend): A specific email backend instance.

        Returns:
            int: Number of successfully delivered messages (1 if successful, 0 otherwise).

        Raises:
            Exception: If neither `message` nor `template_name` is provided.
        """

        # Determine the protocol (http or https) based on whether the request is secure.
        protocol = "https" if request.is_secure() else "http"

        # Get the domain/host from the request (e.g., example.com or localhost:8000).
        domain = request.get_host()

        # Try to fetch the message and template_name from the keyword arguments.
        message = kwargs.get("message")
        template_name = kwargs.get("template_name")

        # Raise an exception if neither message nor template is provided.
        if template_name is None and message is None:
            raise Exception("Please provide a template name or message to send mail.")
        else:
            # Extract template parameters dictionary or set to empty dict.
            template_params = kwargs.get("template_params", {})

            # Add protocol and domain to the template context.
            template_params["protocol"] = protocol
            template_params["domain"] = domain

            # Render HTML message from template if no plain message is provided.
            html_message = render_to_string(template_name=template_name, context=template_params) if message is None else None

        # Extract the subject from kwargs or use default as protocol://domain.
        subject = kwargs.get("subject", f"{protocol}://{domain}")

        # Extract plain text message, stripping tags if message is HTML.
        message = strip_tags(kwargs.get("message"))

        # Sender's email address.
        from_email = kwargs.get("from_email")

        # List of recipient email addresses.
        recipient_list = kwargs.get("recipient_list")

        # Whether to suppress exceptions when sending the email.
        fail_silently = kwargs.get("fail_silently", False)

        # SMTP authentication credentials (optional).
        auth_user = kwargs.get("auth_user", None)
        auth_password = kwargs.get("auth_password", None)

        # Optional EmailBackend instance (used to control how email is sent).
        connection = kwargs.get("connection", None)

        # Send the email using Django's built-in send_mail function.
        return send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
            auth_user=auth_user,
            auth_password=auth_password,
            connection=connection,
            html_message=html_message,
        )

# Create custom 404 view here
class Custom404View(View):
    """
    Custom404View is a class-based view that handles HTTP 404 (Page Not Found) errors.

    This view is designed to render a user-friendly custom 404 error page whenever
    a non-existent URL is accessed in the application.

    Attributes:
        context (dict): A dictionary used to store context data passed to the template.

    Methods:
        get(request, exception=None, *args, **kwargs):
            Handles GET requests for 404 errors and renders a custom 404 template
            with a relevant status code and context.
    """

    # Define a context dictionary to store template context variables.
    context = {}

    def get(self, request, exception=None, *args, **kwargs):
        """
        Handles GET requests triggered by 404 errors.

        This method is automatically called when a 404 error occurs and the
        handler404 is set to this view. It sets the appropriate context,
        renders the 404.html template, and returns an HTTP 404 response.

        Args:
            request (HttpRequest): The HTTP request object.
            exception (Exception, optional): The exception that caused the 404 error.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: A rendered 404 error page with status code 404.
        """

        # Set a title for the 404 error page.
        self.context["title"] = "Page Not Found"

        # Render the 404 error template with the provided context and return a 404 response.
        return render(
            request=request,              # The current HTTP request.
            template_name="404.html",     # Path to the custom 404 template.
            context=self.context,         # Context passed to the template.
            status=404                    # HTTP status code for 'Not Found'.
        )