from django.contrib import admin
from .models import Contact,Product,Order,OrderUpdate  # Ensure the model name matches

admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderUpdate)



