from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def sene():
    subject, from_email, to = 'hello', 'info.xtrader@gmail.com', 'iran581@gmail.com'
    text_content = 'This is an important message.'
    html_content = render_to_string('aboutus.html')
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()