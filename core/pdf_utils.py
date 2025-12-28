from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io


def render_resume_pdf(template_src, context):
    template = get_template(template_src)
    html = template.render(context)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if pdf.err:
        return None

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=ATS_Resume.pdf"

    return response