from django import forms
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.mail import send_mail
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
    FORM_FIELD_CHOICES
)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

# Create your models here.

@register_snippet
class Agency (models.Model):
    name = models.TextField(default='', verbose_name='Nom')

    email = models.EmailField(blank=True, default='')

    city = models.CharField(max_length=125, default='', blank=True, verbose_name='Ville')
    address_1 = models.CharField(max_length=255, default='', blank=True, verbose_name='Adresse ligne 1')
    address_2 = models.CharField(max_length=255, default='', blank=True, verbose_name='Adresse ligne 2')

    phone_cell = models.CharField(max_length=20, default='', blank=True,  verbose_name='Téléphone portable')
    phone_home = models.CharField(max_length=20, default='', blank=True,  verbose_name='Téléphone fixe')

    latitude = models.FloatField(blank=True, default=0)
    longitude = models.FloatField(blank=True, default=0)

    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        MultiFieldPanel([
            FieldPanel('address_1'),
            FieldPanel('address_2'),
            FieldPanel('city'),
        ], heading='Adresse'),
        MultiFieldPanel([
            FieldPanel('phone_cell'),
            FieldPanel('phone_home'),
        ], heading='Téléphones'),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
        ], heading='Coordonées'),
        # InlinePanel('address_1'),
        ImageChooserPanel('photo')
    ]

    def __str__ (self):
        return self.name

    class Meta:
        verbose_name_plural = 'agences'


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class ACMFormField(AbstractFormField):
    page = ParentalKey(
        'ACMContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


"""
Pages
    ContactIndexPage    - As a blank page to have contact/ before my page
    WhoAreWe            - Qui Sommes Nous ?
    ContactPage         - 
"""
class ContactIndexPage (Page):
    
    class Meta:
        verbose_name = 'Contact Index'


class ContactPage(AbstractEmailForm):

    place = models.OneToOneField(
        'widgets.Place',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='contact_place',
        verbose_name='Lieu'
    )

    template = models.CharField(max_length=125, blank=True, default='contact/contact_page.html')

    landing_page_template = models.CharField(max_length=125, blank=True, default='contact/contact_page_landing.html')

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6'),
            ]),
            FieldPanel('subject'),
        ], heading='Paramètres'),
        InlinePanel('form_fields', label='Form Fields'),
        SnippetChooserPanel('place'),
    ]

    promote_panels = AbstractEmailForm.promote_panels + [
        FieldPanel('template'),
        FieldPanel('landing_page_template'),
    ]

    class Meta:
        verbose_name = 'Contact: Formulaire'

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        content = '\n'.join(content)
        send_mail(
            self.subject, content, addresses, self.from_address)


""" Wrong name """
class Who_AreWe (Page):

    agencies = ParentalManyToManyField(
        'contact.Agency',
        blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('agencies', widget=forms.CheckboxSelectMultiple),
        ], heading="Information"),
    ]

    class Meta:
        verbose_name = 'Contact: Qui sommes nous ?'


class ACMContactPage (AbstractEmailForm):

    template = 'contact/acm_contact_page.html'
    
    # Landing page is kinda a template
    landing_page_template = 'contact/contact_page_landing.html'

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6'),
            ]),
            FieldPanel('subject'),
        ], heading='Paramètres'),
        InlinePanel('form_fields', label='Form Fields'),
    ]

    class Meta:
        verbose_name = 'Contact: Demande d\'intervention'

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            print (request.POST)
            form = self.get_form(request.POST, request.FILES, page=self, user=request.user)
            if form.is_valid():
                
                bouble_check = False

                DATA_NAME = 'objet-de-votre-demande'
                DATA_OTHER_NAME = 'objet_de_votre_demande'

                if form.cleaned_data[DATA_NAME] == 'Autre':
                    choix_autre = request.POST.get(DATA_OTHER_NAME, False)
                    if choix_autre:
                        form.cleaned_data[DATA_NAME] = choix_autre
                        bouble_check = True
                    
                    else :
                        form.errors[DATA_NAME] = ['Si Autre, précisez votre choix']
                        form.errors[DATA_OTHER_NAME] = ['Précisez votre choix ici.']

                if bouble_check:
                    form_submission = self.process_form_submission(form)
                    return self.render_landing_page(request, form_submission, *args, **kwargs)

        else:
            form = self.get_form(page=self, user=request.user)

        ctx = self.get_context(request)
        ctx['form'] = form

        return render(
            request,
            self.template,
            ctx
        )

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        content = '\n'.join(content)
        send_mail(
            self.subject, content, addresses, self.from_address)
    

