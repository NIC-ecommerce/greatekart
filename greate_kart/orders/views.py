from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from carts.models import Cart, CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from store.models import Product
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    tax = 0
    grand_total = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity = cart_item.quantity
    tax = (5 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print('valid')
            data = Order()
            print(data)
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.region = form.cleaned_data['region']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            print('save')

            #Generate ORDER NUMBER
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, order_number=order_number, is_ordered=False)
            context ={
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            print(form.errors)
            return redirect('home')


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()


        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_variation)
        order_product.save()
        #Decrease quantity of product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # cart_items.delete()
    #Sending email
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_recieved.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email, ])
    send_email.send()
    #sending data
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,

    }
    return JsonResponse(data)


    return render(request, 'orders/payments.html')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        sub_total = 0
        for product in ordered_products:
            sub_total += product.product_price*product.quantity
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'payment': payment.payment_id,
            'sub_total': sub_total,
        }
        return render(request, 'orders/order_complete.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist, OrderProduct.DoesNotExist):
        return redirect('home')