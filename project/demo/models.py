from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

# Create your models here.

class DemoIndexPage (Page):

    class Meta:
        verbose_name = 'Demo: Index'

class DemoPage1 (Page):
    template = models.CharField(max_length=125, default='demo/demo_page.html')

    promote_panels = Page.promote_panels + [
        FieldPanel('template')
    ]

    class Meta:
        verbose_name = 'Demo: Page Demo 1'