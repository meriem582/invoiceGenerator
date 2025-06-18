from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from invoiceGeneratorApp.models import Product,Invoice,InvoiceItem
from django.core.paginator import Paginator
import json
from .utils import generate_invoice_pdf


# Fonction pour rendre la page d'accueil du tableau de bord
# Cette fonction est appelée lorsque l'utilisateur accède à la page d'accueil de l'application.
def renderDashBoard(request):
    return render(request, 'dashboard.html')


# Fonction pour rendre la page des produits
# Cette fonction récupère tous les produits de la base de données, les pagine en groupes de 15,
# et les envoie à la page 'Product.html' pour affichage.
def renderProduct(request):
    products = Product.objects.all().order_by('id') 
    paginator = Paginator(products, 15)
    
    page_number = request.GET.get('page')
    page_content = paginator.get_page(page_number)
    
    setinfo = {
        'page_content': page_content,
    }
    return render(request, 'product.html', setinfo)

# Fonction pour rendre la page d'édition d'un produit
# Cette fonction récupère un produit spécifique par son ID et le passe à la page 'edit
def renderEdit(request,id):
    product=Product.objects.get(id=id)
    setinfo={
        'product':product,
    }
    return render(request,'edit.html',setinfo)

# Fonction pour ajouter un nouveau produit
# Cette fonction récupère les données du produit à partir de la requête POST,
# crée un nouvel objet Product avec ces données, et le sauvegarde dans la base de données

def addProduct(request):
    name0=request.POST["name"]
    price0=request.POST["price"]
    expiration_date0=request.POST["expiration_date"]
    newProduct=Product(name=name0,price=price0,expiration_date=expiration_date0)
    newProduct.save()
    return HttpResponseRedirect(reverse("product"))

# Fonction pour supprimer un produit
# Cette fonction récupère un produit spécifique par son ID et le supprime de la base de

def deleteProduct(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return HttpResponseRedirect(reverse("product"))

# Fonction pour modifier un produit
# Cette fonction récupère les données du produit à partir de la requête POST,
def EditProduct(request,id):
    Id=request.POST["id"]
    product=Product.objects.get(id=Id)
    name0=request.POST["name"]
    price0=request.POST["price"]
    date0=request.POST["expiration_date"]
    product.name=name0
    product.price=price0
    product.expiration_date=date0
    product.save()
    return HttpResponseRedirect(reverse("product"))

# Cette fonction récupère un produit spécifique par son ID

def searchProduct(request):
    Id=request.POST["idSearched"]
    product=Product.objects.get(id=Id)
    setinfo={
        'productSearched':product,
    }
    return render(request,'modifier.html',setinfo)

# Fonction pour générer une facture
# Cette fonction traite une requête POST contenant des données de produit,
# crée une nouvelle facture et des éléments de facture associés, puis renvoie une réponse JSON.

def generateInvoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Product_data = data.get('products', [])
            
            if not Product_data:
                return JsonResponse({'success': False, 'error': 'No product selected'})
            
            newInvoice = Invoice.objects.create()
            
            for product_data in Product_data:
                product_id = product_data['product_id']
                quantity = int(product_data['quantity'])
                
                product = Product.objects.get(id=product_id)
                InvoiceItem.objects.create(
                    invoice=newInvoice,
                    product=product,
                    quantity=quantity
                )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Not a POST request'})

# Fonction pour rendre la page des factures
# Cette fonction récupère toutes les factures de la base de données, les pagine en groupes de 15

def renderInvoice(request):
    per_page = request.GET.get('per_page', 15)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 15
        
    Invoices = Invoice.objects.all().order_by('-date_created')
    paginator = Paginator(Invoices, per_page)
    
    page_number = request.GET.get('page')
    page_content = paginator.get_page(page_number)
    
    setinfo = {
        'page_content': page_content,
        'per_page': per_page,
    }
    
    return render(request, 'invoice.html', setinfo)

# Fonction pour supprimer une facture
# Cette fonction récupère une facture spécifique par son ID et la supprime de la base de donnée

def deleteInvoice(request,id):
    
    invoice=Invoice.objects.get(id=id)
    invoice.delete()
    return HttpResponseRedirect(reverse("invoice"))

# Fonction pour obtenir les détails d'une facture
def invoice_details(request, id):
    try:
        invoice = Invoice.objects.get(id=id)
        items = invoice.items.all()
        
        data = {
            'invoice_id': invoice.id,
            'date_created': invoice.date_created.strftime("%Y-%m-%d %H:%M"),
            'items': [
                {
                    'product_name': item.product.name,
                    'price': float(item.product.price),
                    'quantity': item.quantity
                }
                for item in items
            ],
            'total': float(invoice.get_total())
        }
        return JsonResponse(data)
    except Invoice.DoesNotExist:
        return JsonResponse({'error': 'Invoice does not exist'}, status=404)
    
# Fonction pour télécharger un PDF de la facture
    
def download_invoice_pdf(request, id):
    try:
        invoice = Invoice.objects.get(id=id)
        items = invoice.items.all()
        
        invoice_data = {
            'invoice_id': invoice.id,
            'date_created': invoice.date_created.strftime("%Y-%m-%d %H:%M"),
            'items': [
                {
                    'product_name': item.product.name,
                    'price': float(item.product.price),
                    'quantity': item.quantity
                }
                for item in items
            ],
            'total': float(invoice.get_total())
        }
        
        buffer = generate_invoice_pdf(invoice_data)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
        return response
        
    except Invoice.DoesNotExist:
        return HttpResponse("Invoice not found", status=404)