from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



#################### index####################################### 
def index(request):
    return render(request, 'accounts/index.html', {'title':'HOME'})

  
########### register here ##################################### 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system #################################### 
            htmly = get_template('accounts/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'title':'register here'})
  
################ login forms################################################### 
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form, 'title':'log in'})

def logout_view(request):
    logout(request)
    # Custom logic, if any
    return redirect('index')

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')


from .models import Blog
from .forms import BlogForm
from django.http import HttpResponseNotFound
from django.urls import reverse
import uuid

@login_required
def add_term(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            # Generate a unique public_url using UUID
            blog.public_url = str(uuid.uuid4())
            blog.save()
            # Redirect to the blog detail view with the correct public_url
            return redirect('index1')  # Change this to the appropriate URL name for your blog list view
    else:
        form = BlogForm()
    return render(request, 'accounts/add_blog.html', {'form': form, 'title': 'ADD FILE'})

@login_required
def index1(request):
    user_blogs = Blog.objects.filter(user=request.user)
    return render(request, 'accounts/index1.html', {'user_blogs': user_blogs, 'title': 'ALL FILES'})
def blog_detail(request, public_url):
    try:
        blog = Blog.objects.get(public_url=public_url)
        return render(request, 'accounts/blog_detail.html', {'blog': blog, 'title': 'FILE'})
    except Blog.DoesNotExist:
        return HttpResponseNotFound('<h1>Blog not found</h1>')
    
def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.public_url)])


from .forms import ContactForm
from django.core.mail import EmailMessage

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f"Message from {name}"
            body = f"Sender's email: {email}\n\nMessage:\n{message}"
            
            # Create and send the email
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=email,  # Sender's email address from the form
                to=['2000031715cse@gmail.com'],  # Replace with your recipient's email address
                reply_to=[email],  # Set the reply-to address to sender's email
            )
            email_message.send()
            
            return redirect('success')  # Display a success page
    else:
        form = ContactForm()
    return render(request, 'accounts/contact.html', {'form': form, 'title': 'CONTACT US'})

def success(request):
    return render(request, 'accounts/success.html',{'title': 'SUCCESS'})

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('index1')  # Redirect to all blogs page
    return render(request, 'accounts/edit_blog.html', {'form': form, 'title': 'EDIT FILE', 'form_title': 'Edit File', 'button_label': 'Update Term'})

def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        blog.delete()
        # Redirect to a suitable page after deleting
        return redirect('index1')
    # return render(request, 'accounts/delete_blog.html', {'blog': blog})

from .forms import UploadPDFForm
from .models import UploadedPDF

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pdf = form.save(commit=False)
            uploaded_pdf.user = request.user
            uploaded_pdf.save()
            uploaded_pdf.public_url = uploaded_pdf.pdf_file.url
            uploaded_pdf.save()
            return redirect('pdf_list')
    else:
        form = UploadPDFForm()
    return render(request, 'accounts/upload_pdf.html', {'form': form})

def pdf_list(request):
    pdfs = UploadedPDF.objects.filter(user=request.user)
    return render(request, 'accounts/pdf_list.html', {'pdfs': pdfs})