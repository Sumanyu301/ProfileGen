import PyPDF2
import re
import logging

logger = logging.getLogger(__name__)

class ResumeOCR:
    """Simple, reliable OCR class for extracting text from PDF documents"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text_from_pdf(self, file_obj):
        """
        Extract text from PDF using PyPDF2 (proven to work well)
        """
        try:
            # Reset file pointer to beginning
            file_obj.seek(0)
            pdf_reader = PyPDF2.PdfReader(file_obj)
            text = ""
            
            # Extract text from all pages
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if text.strip():
                logger.info("Successfully extracted text using PyPDF2")
                return text
            else:
                return "Could not extract text from PDF"
                
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            return "Could not extract text from PDF"

class ResumeParser:
    """Simple, reliable resume parser based on the original working logic"""
    
    def parse_resume(self, text):
        """Parse resume text using the original proven approach with small improvements"""
        
        if not text or text.strip() == "" or text == "Could not extract text from PDF":
            return self._get_empty_result()
        
        # Use the original parsing logic that was working
        
        # Extracting the name (first non-empty line)
        name = text.split('\n')[0].strip() if text.split('\n') else "Name not found"
        
        # Extracting the email with improved error handling
        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        if email_match:
            email = email_match.group(0)
        else:
            email = "Email not found"
        
        # Extracting the phone number
        phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        if phone_match:
            phone = phone_match.group(0)
        else:
            phone = "Phone number not found"
        
        # Education section (improved logic to exclude projects)
        education_split = text.split("Education")
        if len(education_split) > 1:
            education_text = education_split[1]
            # Stop at Experience, Projects, or Skills sections
            for stop_word in ["Experience", "Projects", "Skills"]:
                if stop_word in education_text:
                    education_text = education_text.split(stop_word)[0]
                    break
            education = education_text.strip()
        else:
            education = "Education not found"
        
        # Work experience section (improved logic to include projects)  
        experience_parts = []
        
        # Look for Experience section
        work_experience_split = text.split("Experience")
        if len(work_experience_split) > 1:
            exp_text = work_experience_split[1]
            # Stop at Skills section
            if "Skills" in exp_text:
                exp_text = exp_text.split("Skills")[0]
            experience_parts.append(exp_text.strip())
        
        # Look for Projects section and add to experience (check multiple variations)
        project_keywords = ["Projects", "Project", "Personal Projects", "Academic Projects", "Key Projects"]
        for keyword in project_keywords:
            projects_split = text.split(keyword)
            if len(projects_split) > 1:
                projects_text = projects_split[1]
                # Stop at Skills or other major sections
                for stop_word in ["Skills", "Education", "Certifications", "Awards", "References"]:
                    if stop_word in projects_text:
                        projects_text = projects_text.split(stop_word)[0]
                        break
                if projects_text.strip():
                    experience_parts.append(f"{keyword.upper()}:\n" + projects_text.strip())
                break  # Only use the first match to avoid duplicates
        
        # Combine experience and projects
        if experience_parts:
            work_experience = "\n\n".join(experience_parts)
        else:
            work_experience = "Work Experience not found"
        
        # Skills section (original logic with bug fix)
        skills_split = text.split("Skills")
        if len(skills_split) > 1:
            skills = skills_split[1].strip()
        else:
            skills = "Skills not found"
        
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'education': education,
            'experience': work_experience,
            'skills': skills
        }
    
    def _get_empty_result(self):
        """Return empty result structure"""
        return {
            'name': 'Could not extract',
            'email': 'Could not extract',
            'phone': 'Could not extract',
            'education': 'Could not extract',
            'experience': 'Could not extract',
            'skills': 'Could not extract'
        }
