#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('/home/sumanyu301/Desktop/ProfileGen')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HRMS.settings')
django.setup()

from django.template import Template, Context, TemplateSyntaxError
from django.template.loader import get_template

def validate_template(template_name):
    try:
        template = get_template(template_name)
        print(f"✅ {template_name} - Template syntax is valid")
        return True
    except TemplateSyntaxError as e:
        print(f"❌ {template_name} - Template syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ {template_name} - Other error: {e}")
        return False

# Validate all templates
templates = ['file.html', 'dashboard.html', 'form.html', 'index.html', 'base.html']
for template in templates:
    validate_template(template)
