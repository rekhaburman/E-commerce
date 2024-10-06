from django.shortcuts import render, redirect
from ecommerceapp.models import Contact as ContactModel, Product, Order, OrderUpdate
from django.contrib import messages
from ecommerceapp import keys  # Make sure 'keys' is properly defined
from django.conf import settings
from paypalrestsdk import Payment
import paypalrestsdk 

MERCHANT_KEY = keys.MK
paypalrestsdk.configure({
    "mode": "sandbox",  # "sandbox" for testing, "live" for production
    "client_id": keys.PAYPAL_CLIENT_ID,  # From your PayPal Developer account
    "client_secret": keys.PAYPAL_CLIENT_SECRET  # From your PayPal Developer account
})

def index(request):
    allProds = []
    categories = Product.objects.values('category', 'product_id')
    unique_cats = {item['category'] for item in categories}
    
    for cat in unique_cats:
        products = Product.objects.filter(category=cat)
        allProds.append((products, range(1, len(products)), len(products)))
        
    return render(request, 'index.html', {'allProds': allProds})




def contact_view(request): 
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/login')
    
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        contact = ContactModel(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, "Contact Form is Submitted")
  
    return render(request, 'contact.html')

def about(request):
    return render(request, "about.html")

def checkout_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to proceed with the checkout.')
        return redirect('/auth/login')

    if request.method == 'POST':
        # Capture order details
        item_json = request.POST.get('item_json', '')
        name = request.POST.get('name', '')
        total_amount = request.POST.get('amount', '')  # Use 'total_amount', not 'Totle_amount'
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipcode = request.POST.get('zipcode', '')
        phone = request.POST.get('phone', '')
        print("------------------------------------")
        print(item_json)
        print("------------------------------------")
        # Create a new order in the database
        new_order = Order(name=name, total_amount=float(total_amount), email=email,
                          address1=address1, address2=address2, city=city, state=state, zipcode=zipcode, phone=phone)
        new_order.save()

        # PayPal Payment Integration
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(total_amount),  # PayPal expects amount to be a string
                    "currency": "INR"
                },
                "description": "Luxycart Purchase"
            }],
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/payment/execute",  # PayPal return URL
                "cancel_url": "http://127.0.0.1:8000/payment/cancel"    # PayPal cancel URL
            }
        })

        # Create the payment and handle errors if any
        if payment.create():
            # Save PayPal payment_id in order to track later
            new_order.payment_id = payment.id
            new_order.save()

            for link in payment.links:
                if link.rel == "sb-qczon33089171@business.example.com":
                    # Redirect the user to PayPal for payment approval
                    return redirect("EINvZ4edoaEYeF03Y98gN6SHThuOwvkWDYM0UQRrCFXFCXE3IYRpNOQqzpJnpduuR8W0yK6kKAN_chQS")  # Redirect to the correct approval URL
        else:
            # Handle payment creation errors
            messages.error(request, f"An error occurred: {payment.error.get('message')}")
            return render(request, 'checkout.html')

    # Render the checkout page if request is not POST
    return render(request, 'checkout.html')

def payment_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # Find the payment by PayPal payment ID
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment is successful, update the order status
        order = Order.objects.get(payment_id=payment_id)
        order.status = 'Completed'
        order.save()

        # Add an order update (optional)
        update = OrderUpdate(order_id=order.order_id, update_desc="Your payment has been completed.")
        update.save()

        # Render the payment success page
        return render(request, 'payment.html', {"success": True, "order": order})
    else:
        # Payment failed
        return render(request, 'payment.html', {"success": False})
    
def payment_cancel(request):
    return render(request, 'payment.html', {"success": False})
