import django


django.setup()
from product.models import Category

from encyclopedia.models import ArticleEncyclopedia, ArticleEncyclopediaCategory
from faker import factory, Faker
from model_bakery.recipe import Recipe, foreign_key

fake = Faker('fa_IR')

images = [
    "/shop/image/axe.jpeg",
    "/shop/image/back.png",
    "/shop/image/sf.png",
    "/shop/image/zet.jpeg",
]
import random

# for i in Shop.objects.all():
#     i.image = images[random.randint(0, 3)]
#     i.save()
for j in Category.objects.all():
    for i in range(4):
        author = Recipe(
            Category,
            # category=ArticleEncyclopediaCategory.objects.order_by('?').first(),
            # abstract=fake.text(),
            parent=j,
            # product=i,
            image=images[i % 4]
            # product=Product.objects.order_by("?").first(),
            # capacity=random.uniform(11, 11111),
            # price=random.uniform(11, 11111),
            # inventory_state=random.uniform(0, 2),
            # phone=f"093223324{i}",
            # createdDate=fake.future_datetime(end_date="+30d", tzinfo=None),
            # updatedDate=fake.future_datetime(end_date="+30d", tzinfo=None),
        )
        author.make()
