from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Custom user for future extensibility."""

    pass


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=20, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=50, unique=True, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    region = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    address = models.CharField(max_length=90, blank=True)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}, email: {self.email}")


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        NEW = 'new', 'Нове'
        IN_PROGRESS = 'in_progress', 'В обробці'
        COMPLETED = 'completed', 'Виконано'
        CANCELLED = 'cancelled', 'Скасовано'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.NEW
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        
        super().save(*args, **kwargs)