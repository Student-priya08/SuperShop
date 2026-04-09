from django.shortcuts import render
from .models import Product, Inventory, StockTransaction, Category, Unit
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Sum

# Create your views here.

def dashboard(request):
    total_products = Product.objects.count()
    total_stock = Inventory.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_transactions = StockTransaction.objects.count()
    low_stock_products = Inventory.objects.filter(quantity__lt=10)
    
    # For chart
    import json
    stock_labels = json.dumps([item.product.product_name for item in Inventory.objects.all()])
    stock_data = json.dumps([item.quantity for item in Inventory.objects.all()])
    
    return render(request, 'inventory/dashboard.html', {
        'total_products': total_products,
        'total_stock': total_stock,
        'total_transactions': total_transactions,
        'low_stock_products': low_stock_products,
        'stock_labels': stock_labels,
        'stock_data': stock_data,
    })

def product_list(request):
    query = request.GET.get('search')
    products = Product.objects.all()

    if query:
        products = products.filter(product_name__icontains=query)

    return render(request, 'inventory/products.html', {'products': products, 'request': request})

def inventory_list(request):
    query = request.GET.get('search')
    inventory = Inventory.objects.all()

    if query:
        inventory = inventory.filter(product__product_name__icontains=query)

    return render(request, 'inventory/inventory.html', {'inventory': inventory, 'request': request})

def transaction_list(request):
    transactions = StockTransaction.objects.all().order_by('-transaction_date')
    return render(request, 'inventory/transactions.html', {'transactions': transactions})

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        unit_id = request.POST.get('unit')
        
        if product_name and price and category_id:
            category = Category.objects.get(id=category_id)
            unit = Unit.objects.get(id=unit_id) if unit_id else None
            Product.objects.create(product_name=product_name, price=price, category=category, unit=unit)
            messages.success(request, 'Product added successfully!')
            return redirect('products')
    
    categories = Category.objects.all()
    units = Unit.objects.all()
    return render(request, 'inventory/add_product.html', {'categories': categories, 'units': units, 'request': request})

def add_transaction(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        transaction_type = request.POST.get('transaction_type')
        quantity = request.POST.get('quantity')
        
        if product_id and transaction_type and quantity:
            try:
                product = Product.objects.get(id=product_id)
                quantity = int(quantity)
                
                # Validate quantity is not negative
                if quantity <= 0:
                    messages.error(request, 'Quantity must be greater than 0!', extra_tags='danger')
                    return redirect('add_transaction')
                
                # For OUT transactions, check if we have enough stock
                if transaction_type == 'OUT':
                    try:
                        inventory = Inventory.objects.get(product=product)
                        if inventory.quantity < quantity:
                            messages.error(request, f'Not enough stock! Available: {inventory.quantity}', extra_tags='warning')
                            return redirect('add_transaction')
                    except Inventory.DoesNotExist:
                        messages.error(request, 'No stock record for this product!', extra_tags='danger')
                        return redirect('add_transaction')
                
                # Create transaction
                StockTransaction.objects.create(
                    product=product, 
                    transaction_type=transaction_type, 
                    quantity=quantity
                )
                messages.success(request, 'Transaction added successfully!', extra_tags='success')
                return redirect('transactions')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found!', extra_tags='danger')
                return redirect('add_transaction')
            except ValueError:
                messages.error(request, 'Invalid quantity!', extra_tags='danger')
                return redirect('add_transaction')
    
    products = Product.objects.all()
    return render(request, 'inventory/add_transaction.html', {'products': products, 'request': request})

# Category Management Views
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        
        if category_name:
            Category.objects.create(category_name=category_name)
            messages.success(request, 'Category added successfully!')
            return redirect('categories')
    
    return render(request, 'inventory/add_category.html')

def edit_category(request, id):
    category = Category.objects.get(id=id)
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        
        if category_name:
            category.category_name = category_name
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories')
    
    return render(request, 'inventory/add_category.html', {'category': category})

def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('categories')

# Unit Management Views
def units_list(request):
    units = Unit.objects.all()
    return render(request, 'inventory/units.html', {'units': units})

def add_unit(request):
    if request.method == 'POST':
        unit_name = request.POST.get('unit_name')
        abbreviation = request.POST.get('abbreviation')
        
        if unit_name and abbreviation:
            Unit.objects.create(unit_name=unit_name, abbreviation=abbreviation)
            messages.success(request, 'Unit added successfully!')
            return redirect('units')
    
    return render(request, 'inventory/add_unit.html')

def edit_unit(request, id):
    unit = Unit.objects.get(id=id)
    
    if request.method == 'POST':
        unit_name = request.POST.get('unit_name')
        abbreviation = request.POST.get('abbreviation')
        
        if unit_name and abbreviation:
            unit.unit_name = unit_name
            unit.abbreviation = abbreviation
            unit.save()
            messages.success(request, 'Unit updated successfully!')
            return redirect('units')
    
    return render(request, 'inventory/add_unit.html', {'unit': unit})

def delete_unit(request, id):
    unit = Unit.objects.get(id=id)
    unit.delete()
    messages.success(request, 'Unit deleted successfully!')
    return redirect('units')
