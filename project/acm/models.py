from django import forms
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from rest_framework import status

from wagtail.snippets.models import register_snippet
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

from core.models import SEOPage
from widgets.models import School
from widgets.serializers import SchoolSerializer


class ProgramManager (models.Manager):

    def get_types (self):
        pass 

@register_snippet
class Program (models.Model):
    name = models.CharField(max_length=50, default='0', verbose_name='Nom')
    TYPE_CHOICES = (
         (1, 'MOINS6'),
         (2, 'PLUS6'),
       # (3, 'JEANNE MERTON'),
       # (4, 'EDOUARD MARCEAU'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, default=0)

    comment = models.TextField(blank=True, default='', verbose_name='Note additionelle')

    file_drive = models.URLField(blank=True, default='', verbose_name='Lien Google Drive')

    file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Fichier'
    )

    objects = ProgramManager()

    panels = [
        FieldPanel('name'),
        FieldPanel('type'),
        FieldPanel('comment'),
        FieldPanel('file_drive'),
        DocumentChooserPanel('file')
    ]

    @staticmethod
    def get_types ():
        return dict(Program.TYPE_CHOICES)

    class Meta:
        ordering = ['type']

    def __str__ (self):
        return f'#{self.id} - {self.name} - {dict(self.TYPE_CHOICES).get(self.type)}'


"""
Pages
"""

""" To be deleted """
class TarifsEtHorairesPage (Page):
    template = models.CharField(max_length=250, blank=True, default='acm/tarifs_et_horaires_page.html')

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('template'),
    ]

    class Meta:
        verbose_name = 'ACM: Dynamic page for Tarifs or Horaires'


class ProgramsPage (SEOPage):
    programs = ParentalManyToManyField(
        'acm.Program',
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('programs', widget=forms.CheckboxSelectMultiple)
    ]

    class Meta:
        verbose_name = 'ACM: Programmes ACM'


""" Signup guide page for ACM services """
class ChildSignupGuidePage (SEOPage):

    template = models.CharField(max_length=250, blank=True, default='acm/guide_inscription_page.html')

    promote_panels = SEOPage.promote_panels + [
        FieldPanel('template'),
    ]

    class Meta:
        verbose_name = 'ACM: Guide d\'inscription'


class SchoolsPage (SEOPage):

    schools = ParentalManyToManyField(
        'widgets.School',
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('schools', widget=forms.CheckboxSelectMultiple)
    ]

    def json (self):
        return SchoolSerializer(self.schools, many=True).data

    class Meta:
        verbose_name = 'ACM: Ecoles'


class SchoolsAPIPage (Page):

    class Meta:
        verbose_name = 'ACM: Ecoles API'

    def serve(self, request, *args, **kwargs):
        response_object = {'status': 'Failure'}

        if request.method == 'GET':
            id = request.GET.get('id', False)

            if id:
                school = get_object_or_404(School, id=id)
                response_object['status'] = 'Success'
                response_object['school'] = SchoolSerializer(school).data

            else:
                schools = School.objects.all()

                print (response_object)

                response_object['status'] = 'Success'
                response_object['schools'] = SchoolSerializer(schools, many=True).data
                # setattr(response_object, 'status', 'Success')
                # setattr(response_object, 'schools', SchoolSerializer(schools, many=True).data)

            return JsonResponse(response_object, status=status.HTTP_200_OK)

        return JsonResponse(response_object, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                

