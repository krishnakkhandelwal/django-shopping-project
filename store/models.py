from django.db import models

# Create your models here.
#id is created automatically is primary too

class Collection(models.Model):
    number_of_products = models.IntegerField()
    title = models.CharField(max_length=255)
    #circular dependency
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null =True,related_name='+') 
    

#many to many relationship

class Promotion(models.Model):
    description= models.CharField(max_length=255)
    discount=models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    #slug in address bar, for seo  
    slug =  models.SlugField(default='-')#or null=True
    description = models.TextField()
    unit_price= models.DecimalField(decimal_places=2,max_digits=10)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotion=models.ManyToManyField(Promotion, related_name='products')#default-> product_set

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=20)
    birth_date =models.DateField(null=True, blank=True)

    mem_bronze='B'
    Membership_choice=[
        (mem_bronze,'bronze'),
        ('S','Silver'),
        ('G','Gold')
    ]
    
    membership =models.CharField(max_length=1,choices=Membership_choice,default=mem_bronze)

    class Meta:
        db_table = 'store_customers'
        indexes =[
            models.Index(fields=['last_name','first_name'])
        ]



class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)

    pending='P'
    Complete='C'
    Failed='F'
    payment_choices =[
        (pending,'Pending'),
        (Complete,'Complete'),
        (Failed,'Failed'),

    ]
    payment_status = models.CharField(max_length=1, choices=payment_choices, default=pending)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)

    


#1-1 relation with customers
class address(models.Model):
    
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) # setdefault , protect(unless child is deleted parent cant),setnull

#1-N relation with customers
# class address(models.Model):
    
#     street=models.CharField(max_length=255)
#     city=models.CharField(max_length=255)
#     customer=models.ForeignKey(Customer,on_delete=models.CASCADE ) 



class order_item(models.Model):
    qunatity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    order=models.ForeignKey(Order,on_delete=models.PROTECT)

class Cart(models.Model):
    created_at= models.DateTimeField(auto_now_add=True)

class cart_items(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.PositiveSmallIntegerField()


