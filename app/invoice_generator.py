import os
import sys
import pdfkit
import re
from jinja2 import Environment, FileSystemLoader

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def generate_invoice(data, config):
    # Load Jinja2 template
    templates_path = resource_path('templates')
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template('invoice_template.html')

    # Render HTML
    html = template.render(
        **data,
        **config,
        logo=resource_path(config["logo_path"])
    )

    # Ensure output folder exists
    output_dir = resource_path('invoices')
    os.makedirs(output_dir, exist_ok=True)

    # Sanitize filename
    safe_invoice_number = re.sub(r'[^\w\-]', '_', data['invoice_number'])
    output_path = os.path.join(output_dir, f"{safe_invoice_number}.pdf")

    # Configure pdfkit
    wkhtmltopdf_exe = resource_path('wkhtmltopdf.exe')  # or 'wkhtmltopdf' on Mac/Linux
    pdf_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_exe)

    # Generate PDF
    pdfkit.from_string(html, output_path, configuration=pdf_config, options={"enable-local-file-access": ""})

    return output_path
