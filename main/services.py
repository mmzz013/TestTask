from django.core.mail import send_mail

from .models import User
from DatingSite.settings import EMAIL_HOST_USER


def handle_match_request(user, client_id):
    client = User.objects.get(id=client_id)

    is_mutual_like = client.liked_users.filter(id=user.id).exists()
    if is_mutual_like:
        subject = "Вы понравились!"
        body1 = f"Вы понравились {user.first_name}! Почта участника: {client.email}"
        body2 = f"Вы понравились {client.first_name}! Почта участника: {user.email}"
        send_mail(subject, body1, EMAIL_HOST_USER, [client.email])
        send_mail(subject, body2, EMAIL_HOST_USER, [client.email])

        return client.email
    else:
        user.liked_users.add(client)
        return None
