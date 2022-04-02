from django.contrib.auth import authenticate
from django.shortcuts import redirect, render

from wagtail.documents.views import serve

from .forms import PortalForm, LoginForm
from .models import Auth

# Create your views here.

def auth_demo(request):
    return render(request, 'Auth/base.html', {'form4: True'})

def auth_portal (request):
    ctx = {}

    email = request.session.get('email', False)
    if email:
        ctx['email'] = email    
        del request.session['email']

    if request.method == 'POST':
        f = PortalForm(request.POST)
        if f.is_valid():
            try:
                Auth.objects.get(email=f.cleaned_data['email'])
                view = 'user:auth_login'
            except Auth.DoesNotExist:
                view = 'user:auth_signup'

            request.session['email'] = f.cleaned_data['email']
            return redirect(view)

        ctx['errors'] = ['Veuillez saisir une adresse email.']   

    return render(request, 'Auth/Portal.html', ctx)

def auth_login (request):
    email = request.session.get('email', False)
    if not email:
        return redirect('user:auth_portal')

    ctx = {'email': email}

    if request.method == 'POST':
        password = request.POST.get('password', False)
        if password:
            auth = authenticate(email=email, password=password)
            if auth:
                return redirect('')
            
            ctx['errors'] = ['Identifiants invalides.']
    
    return render(request, 'Auth/Login.html', ctx)

def auth_signup (request):
    email = request.session.get('email', False)
    if not email:
        return redirect('user:auth_portal')
    
    print (email)
    ctx = {'email': email, 'form3': True}

    return render(request, 'Auth/Signup.html', ctx)


def view_document(request, document_id, document_filename):
    """
    Calls the normal document `serve` view, except makes it not an attachment.
    """
    # Get response from `serve` first
    response = serve.serve(request, document_id, document_filename)

    # Remove "attachment" from response's Content-Disposition
    contdisp = response['Content-Disposition']
    response['Content-Disposition'] = "; ".join(
        [x for x in contdisp.split("; ") if x != "attachment"]
    )

    return response