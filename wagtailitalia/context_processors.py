from django.conf import settings as django_settings


def base_settings(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'PROJECT_NAME': django_settings.PROJECT_NAME}
