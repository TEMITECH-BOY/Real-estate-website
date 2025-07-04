from django.core.mail import send_mail
from django.conf import settings

def sendMail(email, fullname):
    subject = 'Welcome to Real Estate App'
    message = f'Hello {fullname},\n\nThank you for registering with us! We are excited to have you on board.\n\nBest regards,\nReal Estate Team'
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],  # ✅ FIXED: only pass email here
        fail_silently=False,
    )
