import os
import io
import tempfile
from matplotlib import pyplot as plt
from fpdf import FPDF
from crewai.tools import tool

@tool
def generate_analysis_graphics_tool(data_to_analyze: dict, report_text: str) -> str:
    """
    Generates a polished PDF report including the agent's text analysis and meaningful performance charts.
    """
    
    output_dir = os.path.abspath("outputs")
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "relatorio_desempenho_sistema.pdf")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # First page: report
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Relatório de Desempenho do Sistema", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for line in report_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    def save_chart_to_tempfile(fig) -> str:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        fig.savefig(temp.name, format='png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        return temp.name

    def center_image_on_pdf(pdf, chart_path, w):
        # Center the image both vertically and horizontally on the page
        page_width = pdf.w - 2 * pdf.l_margin
        page_height = pdf.h - 2 * pdf.t_margin
        image_height = 150 * 0.75  # estimated from width since it's proportional
        x = (page_width - w) / 2 + pdf.l_margin
        y = (page_height - image_height) / 2 + pdf.t_margin
        pdf.image(chart_path, x=x, y=y, w=w)

    # ---------- PIE CHART ----------
    labels = ['Aprovados', 'Recusados']
    values = [data_to_analyze['total_items_approved'], data_to_analyze['total_items_refused']]
    colors = ['#4CAF50', '#F44336']

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        values,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.5)
    )
    ax.axis('equal')
    ax.set_title("Distribuição de Aprovações e Recusas", pad=40)

    # Add labels manually centered below chart
    ax.legend(wedges, labels, title="Status", loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2)

    chart_path = save_chart_to_tempfile(fig)
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Gráfico: Aprovações e Recusas", ln=True, align="C")
    center_image_on_pdf(pdf, chart_path, w=150)
    os.unlink(chart_path)

    # ---------- BAR CHART: Correções por Campo ----------
    changes = data_to_analyze["field_change_ranking"]
    field_names = list(changes.keys())
    total_changes = [changes[k]["total_changes_across_items"] for k in field_names]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(field_names, total_changes, color='skyblue')
    ax.set_xlabel("Total de Correções")
    ax.set_title("Campos com Mais Correções")
    chart_path = save_chart_to_tempfile(fig)
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Gráfico: Campos com mais correções", ln=True, align="C")
    center_image_on_pdf(pdf, chart_path, w=180)
    os.unlink(chart_path)

    # ---------- BAR CHART: Correções por Item ----------
    item_ids = list(data_to_analyze['items_timeline'].keys())
    corrections_per_item = [data_to_analyze['items_timeline'][i]['total_fields_changed'] for i in item_ids]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(item_ids, corrections_per_item, color='orange')
    ax.set_xlabel("ID do Item")
    ax.set_ylabel("Correções no Item")
    ax.set_title("Correções por Item Analisado")
    chart_path = save_chart_to_tempfile(fig)
    pdf.add_page()
    pdf.cell(0, 10, "Gráfico: Correções por Item", ln=True, align="C")
    center_image_on_pdf(pdf, chart_path, w=170)
    os.unlink(chart_path)

    # ---------- BAR CHART: Precisão Geral ----------
    correct = data_to_analyze["global_ai_accuracy"]["total_fields_correct"]
    corrected = data_to_analyze["global_ai_accuracy"]["total_fields_corrected"]

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(["Corretos", "Corrigidos"], [correct, corrected], color=['#4CAF50', '#FFC107'])
    ax.set_title("Precisão Geral dos Campos")
    ax.set_ylabel("Quantidade de Campos")
    chart_path = save_chart_to_tempfile(fig)
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Gráfico: Precisão Global dos Campos", ln=True, align="C")
    center_image_on_pdf(pdf, chart_path, w=150)
    os.unlink(chart_path)

    pdf.output(pdf_path)
    return pdf_path
