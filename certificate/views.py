from django.shortcuts import render,HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from .models import Certificate
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.
def generate_certificate(request):
    
    if request.method=='POST':
        user=request.POST.get('user')
        quiz_title= request.POST.get('quiz_title')
        score = request.POST.get('score')

        template_path = 'certificate/gen_certificate.html'
        context = {
                'user': user,
                'quiz_title': quiz_title,
                'score': score,
                'date': 'April 1, 2024'  # You can add more dynamic data as needed
            }
        certificate_content = get_template(template_path).render(context)
        pdf_file = os.path.join(settings.MEDIA_ROOT, 'certificates', f'{user}_{quiz_title}_certificate.pdf')

        
        with open(pdf_file, 'wb') as file:
                pisa_status = pisa.CreatePDF(certificate_content, dest=file)
            
        if not pisa_status.err:
                # Save the certificate (this assumes you have a Certificate model)
                certificate = Certificate.objects.create(
                    user=user,
                    test_name=quiz_title,
                    score=score,
                    certificate_file=pdf_file
                )
                return HttpResponse("Certificate generated and saved successfully!")
        else:
                return HttpResponse("Error generating PDF.")
    else:
        return HttpResponse("POST request required.")


def send_certificate_email(request, certificate_id):
    try:
        # Retrieve the certificate object
        certificate = Certificate.objects.get(pk=certificate_id)

        # Prepare email content
        subject = 'Your Certificate for Completing the Quiz'
        message = 'Please find your certificate attached.'
        from_email = 'your_email@example.com'
        to_email = certificate.user.email

        # Render email body
        email_body = render_to_string('certificate/certificate_email.html', {'user': certificate.user})

        # Create email message
        email = EmailMessage(subject, message, from_email, [to_email])
        email.attach_file(certificate.certificate_file.path)  # Attach the certificate PDF file
        email.content_subtype = 'html'  # Set email content type to HTML
        email.attach_alternative(email_body, "text/html")  # Attach HTML content

        # Send email
        email.send()

        return HttpResponse("Certificate sent successfully to {}".format(to_email))
    except Exception as e:
        return HttpResponse("Error sending certificate: {}".format(str(e)))