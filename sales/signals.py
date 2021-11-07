from .models import Sale
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Sale.positions.through)
def calculate_total_price(sender, instance, action, **kwargs):
    print(action)
    print(instance)

    totalPrice = 0
    if action == 'post_add' or action == 'post_remove':
        for item in instance.get_positions():
            totalPrice += item.price

    instance.total_price = totalPrice
    instance.save()