from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch

def generate_invoice_pdf(invoice_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Définir les marges
    left_margin = 1 * inch
    right_margin = 1 * inch
    usable_width = letter[0] - left_margin - right_margin
    
    # En-tête centré
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0]/2, 10.5*inch, f"Invoice #{invoice_data['invoice_id']}")
    p.setFont("Helvetica", 12)
    p.drawCentredString(letter[0]/2, 10*inch, f"Date: {invoice_data['date_created']}")
    
    # Séparateur
    p.line(left_margin, 9.8*inch, letter[0]-right_margin, 9.8*inch)
    
    # Données du tableau
    data = [["Product", "Price", "Quantity", "Total"]]
    for item in invoice_data['items']:
        total = item['price'] * item['quantity']
        data.append([
            item['product_name'],
            f"{item['price']:.2f} €",
            str(item['quantity']),
            f"{total:.2f} €"
        ])
    
    # Création du tableau avec largeurs de colonnes proportionnelles
    col_widths = [
        usable_width * 0.5,  # 50% pour Product
        usable_width * 0.2,  # 20% pour Price
        usable_width * 0.15, # 15% pour Quantity
        usable_width * 0.15  # 15% pour Total
    ]
    
    table = Table(data, colWidths=col_widths)
    
    # Style du tableau
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3A4F7A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F5F5F5')),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    # Positionnement du tableau
    table.wrapOn(p, usable_width, 0)
    table.drawOn(p, left_margin, 7*inch)  # Position Y ajustée
    
    # Total
    p.setFont("Helvetica-Bold", 14)
    total_text = f"Total: {invoice_data['total']:.2f} €"
    p.drawRightString(letter[0]-right_margin, 6.5*inch, total_text)
    
    # Pied de page
    p.setFont("Helvetica", 10)
    p.drawCentredString(letter[0]/2, 0.5*inch, "Invoice Generated with InvoiceGenerator!")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer