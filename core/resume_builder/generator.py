"""
Resume PDF Generator for CareerAI.

This module handles the dynamic creation of ATS-friendly PDF resumés.
It uses 'xhtml2pdf' to convert Django HTML templates into PDF documents.

Author: Naresh Reddy
"""

from django.http import HttpResponse
from django.template.loader import get_template
import io


def render_resume_pdf(template_src, context):
    """
    Renders an HTML template into a downloadable PDF response.
    
    Args:
        template_src (str): Path to the Django HTML template (e.g., 'resume/template.html').
        context (dict): The data dictionary to populate the template.
        
    Returns:
        HttpResponse: A PDF file response for download, or None if error.
    """
    try:
        # Load and render the template with context data
        template = get_template(template_src)
        html = template.render(context)

        # Create a PDF file in memory
        result = io.BytesIO()
        from xhtml2pdf import pisa
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode("UTF-8")), 
            result
        )

        if pdf.err:
            return None

        # Prepare HTTP response with PDF content
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        
        # Force download with a generic filename
        response["Content-Disposition"] = "attachment; filename=ATS_Resume.pdf"

        return response
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
