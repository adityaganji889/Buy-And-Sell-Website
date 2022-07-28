from math import prod
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from requests import session
from .models import Product,OrderDetail
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
import stripe
# Create your views here.
def index(request):
    return HttpResponse('Hello World')

def products(request):
    page_obj = products = Product.objects.all()
    product_name = request.GET.get('product_name')
    if product_name!='' and product_name is not None:
        page_obj = products.filter(name__icontains=product_name)
    paginator = Paginator(page_obj,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request,'myapp/index.html',context)

# CLass based view for above products view (ListView)
class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    paginate_by = 3

def product_detail(request,id):
    product = Product.objects.get(id=id)
    context = {
        'product':product
    }
    return render(request,'myapp/details.html',context)

# CLass based view for above product detail view (ListView)
class ProductDetailView(DetailView):
      model = Product
      template_name = 'myapp/details.html'
      context_object_name = 'product'
      pk_url_kwarg = 'pk'

      def get_context_data(self,**kwargs):
          context = super(ProductDetailView,self).get_context_data(**kwargs)
          context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
          return context

@login_required
def add_product(request):
    if request.method=='POST':
       name = request.POST.get('name')
       price = request.POST.get('price')
       desc = request.POST.get('desc')
       image = request.FILES['upload']
       seller_name = request.user
       product = Product(name=name,price=price,desc=desc,image=image,seller_name=seller_name)
       product.save()
    return render(request,'myapp/addproduct.html')

# CLass based view for creating a product
# @login_required
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'desc', 'image', 'seller_name']
    # 'product_form.html'

def update_product(request,id):
    product = Product.objects.get(id=id)
    if request.method=='POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.desc = request.POST.get('desc')
        product.image = request.FILES['upload']
        product.save()
        return redirect('/myapp/products/')
    context = {
        'product':product,
    }
    return render(request,'myapp/updateproduct.html',context)

# CLass based view for updating a product
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'desc', 'image', 'seller_name']
    template_name_suffix = '_update_form'

def delete_product(request,id):
    product = Product.objects.get(id=id)
    context = {
        'product':product,
    }
    if request.method=='POST':
        product.delete()
        return redirect('/myapp/products/')
    return render(request,'myapp/delete.html',context)
# Class based Delete View
class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('myapp:products')
    context_object_name = 'product'
    template_name_suffix = '_confirm_delete'
def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context={
        'products':products,
    }
    return render(request,'myapp/mylistings.html',context)

@csrf_exempt
def create_checkout_session(request,id):
    products = Product.objects.exclude(seller_name=request.user)
    product = get_object_or_404(products, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':int(product.price*100),
                },
                'quantity':1,
            }
        ],    
            mode='payment',
            success_url = request.build_absolute_uri(reverse('myapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = request.build_absolute_uri(reverse('myapp:failed')),
    )

    order=OrderDetail()
    order.customer_username = request.user.username
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price*100)
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name = 'myapp/payment_success.html'
    
    def get(self,request,*args,**kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        session = stripe.checkout.Session.retrieve(session_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail,stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request,self.template_name)

class PaymentFailedView(TemplateView):
    template_name = 'myapp/payment_failed.html'
