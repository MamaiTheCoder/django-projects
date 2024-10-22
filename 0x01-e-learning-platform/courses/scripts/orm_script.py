from django.contrib.contenttypes.models import ContentType
from django.db import connection

def run():
    content_types = ContentType.objects.all()
    print([c.model_class for c in content_types])