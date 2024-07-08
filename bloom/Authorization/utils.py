from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.dispatch import receiver
from user.models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

@api_view(('POST',))     
def send_reset_Password_mail_user(request):
    try:
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    token = Token.objects.get_or_create(user=user)
    context = {'username': user.username, 'token': token[0]}
    rendered = render_to_string("auth/resetPW.html", context)
    subject = 'captureVue:Reset your Password'
    email_from = settings.EMAIL_HOST_USER
    recipients = [user.email]
    send_mail(subject, '',  email_from, recipients, html_message=rendered)
    return Response({'message':'Reset password mail send successfully'})

def send_register_mail_to_newuser(user,token):
    context = {'username': user.username, 'token': token}
    rendered = render_to_string("auth/signup.html", context)
    subject = 'Welcome to captureVue'
    html_message = rendered
    email_from = 'noreply@capturevue.de'
    recipient_list = [user.email]
    
    send_mail(subject, '',  email_from, recipient_list, html_message=html_message)

@api_view(('GET',))
def activate_user(request, token):
    user = get_object_or_404(CustomUser, auth_token=token)
    user.is_active = True
    user.save()
    return Response({'message': 'User activated successfully.'})

@api_view(('GET',))
def logout_user(request, token):
    token_to_delete = get_object_or_404(Token, key=token)
    token_to_delete.delete()
    
    return Response({'message': 'User logged out successfully.'})


@api_view(('POST',))     
def reset_password(request,token):
    pw1 = request.data.get('pw1')
    pw2 = request.data.get('pw2')
    if pw1 != pw2:
        return Response({'message':'Passwort stimmt nicht mit Passwort2 überein!'})

    user = CustomUser.objects.get(auth_token=token)
    user.set_password(pw1)
    user.save()
    return Response({'message':'Password successfully changed!'})