from django.core.mail import send_mail

from aviasales.celery import app


@app.task
def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
    message = f"""
        Thank you for signing up.
        Please, activate your account.
        Activation link: {activation_url}
    """
    send_mail(
        'Activate your account',
        message,
        'mm.marsel17@gmail.com',
        [email, ],
        fail_silently=False
    )


@app.task
def send_reset_email(email, activation_code):
    activation_url = f'{activation_code}'
    message = f"""Use code to restore password: {activation_url}"""
    send_mail(
        'Reset password',
        message,
        'mm.marsel17@gmail.com',
        [email],
        fail_silently=False,
    )

