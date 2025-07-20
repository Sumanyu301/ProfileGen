import PyPDF2
import re
from django.shortcuts import render ,HttpResponse,redirect
from datetime import datetime
from Home.models import Form,File
from Home.enhanced_ocr_new import ResumeOCR, ResumeParser
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    context = {
      'variable': 'THIS IS VARIABLE PLACEHOLDER'
    }
    return render(request,'index.html',context)


def about(request):
  return HttpResponse("This is about")


def form(request):
  if request.method == "POST":
      name = request.POST.get('name')
      email = request.POST.get('email')
      phone = request.POST.get('phone')
      experience = request.POST.get('experience')
      education = request.POST.get('education')
      skills = request.POST.get('skills')
      varForm = Form(name = name, email= email, phone = phone , education = education, experience=experience,
                  skills=skills)
      varForm.save()
      context = {
        'name' : name,
        'email': email,
        'phone':phone,
        'experience':experience,
        'education':education,
        'skills':skills
      }
      return render(request,'dashboard.html',context)

  return render(request,'form.html')

def dashboard(request):
  return render(request,'dashboard.html')

def contact(request):
    return render(request,'contact.html')


def file(request):
    if request.method=="POST":
        uploaded_file = request.FILES['file']
        File.objects.create(file=uploaded_file)
        
        try:
            # Check if it's a PDF file
            filename = uploaded_file.name
            if not filename.lower().endswith('.pdf'):
                context = {
                    'error': 'Please upload a PDF file only.',
                    'name': 'Error',
                    'email': 'Unsupported format',
                    'phone': 'Unsupported format',
                    'work_experience': 'Unsupported format',
                    'education': 'Unsupported format',
                    'skills': 'Unsupported format'
                }
                return render(request, 'file.html', context)
            
            # Initialize the OCR and parser
            ocr = ResumeOCR()
            parser = ResumeParser()
            
            # Extract text using simple, reliable PyPDF2 approach
            logger.info(f"Starting text extraction from PDF: {filename}")
            text = ocr.extract_text_from_pdf(uploaded_file)
            
            if text == "Could not extract text from PDF":
                context = {
                    'error': 'Could not extract text from the PDF. Please ensure the file contains readable text.',
                    'name': 'Error',
                    'email': 'Could not extract',
                    'phone': 'Could not extract',
                    'work_experience': 'Could not extract',
                    'education': 'Could not extract',
                    'skills': 'Could not extract'
                }
                return render(request, 'file.html', context)
            
            # Parse the extracted text using the proven approach
            logger.info("Parsing extracted text for resume information")
            parsed_data = parser.parse_resume(text)
            
            context = {
                'name': parsed_data['name'],
                'email': parsed_data['email'],
                'phone': parsed_data['phone'],
                'work_experience': parsed_data['experience'],
                'education': parsed_data['education'],
                'skills': parsed_data['skills']
            }
            
            logger.info("Successfully processed PDF resume")
            return render(request, 'dashboard.html', context)
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            context = {
                'error': f'An error occurred while processing the file: {str(e)}',
                'name': 'Error',
                'email': 'Processing failed',
                'phone': 'Processing failed',
                'work_experience': 'Processing failed',
                'education': 'Processing failed',
                'skills': 'Processing failed'
            }
            return render(request, 'file.html', context)
    
    return render(request, 'file.html')

