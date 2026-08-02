from django.conf import settings
from django.template.loader import render_to_string

from weasyprint import HTML

from training.models import TrainingRegister

DOC_CODE = 'SGQ-FOR-017'
DOC_REVISION = 'R03: 23/11/2023'

MIN_ROWS = 20


def build_training_register_rows(registers, min_rows=MIN_ROWS):
    """
    Recebe um queryset/list de TrainingRegister e completa com linhas em
    branco (None) até `min_rows`, pro template desenhar a tabela do mesmo
    jeito que a planilha (linhas vazias com o checkbox "(  ) Eficaz").
    """
    rows = list(registers)
    blanks_needed = max(0, min_rows - len(rows))
    rows += [None] * blanks_needed
    return rows


def render_training_register_html(employee, registers=None):
    """
    Renderiza o HTML do formulário SGQ-FOR-017 pra um colaborador.
    """
    if registers is None:
        registers = (
            TrainingRegister.objects
            .filter(employee=employee, delete=False)
            .select_related('training_type')
            .order_by('aplication_data_training')
        )

    rows = build_training_register_rows(registers)

    return render_to_string('partials/sgq17.html', {
        'employee': employee,
        'company': employee.company,
        'rows': rows,
        'doc_code': DOC_CODE,
        'doc_revision': DOC_REVISION,
    })


def generate_training_register_pdf(employee, registers=None):
    """
    Gera o PDF do formulário SGQ-FOR-017 pra um colaborador.
    Retorna os bytes do PDF, prontos pra HttpResponse ou pra salvar em disco.
    """
    html_string = render_training_register_html(employee, registers)
    pdf_bytes = HTML(string=html_string, base_url=str(settings.BASE_DIR)).write_pdf()
    return pdf_bytes