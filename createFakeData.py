import uuid

import django

django.setup()

from account.models import User
from shop.models import Shop, ShopImage, ShopProduct

from banner.models import Banner


from product.models import ClassId, Product, Category, ProductUnit, ProductImage
from encyclopedia.models import ArticleEncyclopediaCategory, ArticleReference, ArticleEncyclopedia

from doctor.models import DockterBranch, History
from city.models import Country, City, CityLocation
from faker import Faker
from model_bakery.recipe import Recipe

fake = Faker('fa_IR')

images = [
    "/shop/image/axe.jpeg",
    "/shop/image/back.png",
    "/shop/image/sf.png",
    "/shop/image/zet.jpeg",
]

# for i in Shop.objects.all():
#     i.image = images[random.randint(0, 3)]
#     i.save()

# for j in Product.objects.all():
for i in Category.objects.all():
    for k in range(3):
        author = Recipe(
            Category,
            parent=i,
            # product=Product.objects.order_by('?').first(),
            # user=User.objects.order_by('?').first(),
            # category=Category.objects.order_by('?').first(),
            # class_id=ClassId.objects.order_by('?').first(),
            # unit=ProductUnit.objects.order_by('?').first(),
            # parent=fake.text(),
            # parent=ArticleEncyclopediaCategory.objects.order_by("?").first(),
            image=images[k%4],
            # national_code=uuid.uuid4()
            # product=i,
            # abstract="2rweqsdfasfasdf",
            # content="2rweqsdfasfasdf",
            # image=images[j % 4],
            # product=Product.objects.order_by("?").first(),
            # capacity=random.uniform(11, 11111),
            # price=random.uniform(11, 11111),
            # inventory_state=random.uniform(0, 2),
            # phone=f"093223324{i}",
            # createdDate=fake.future_datetime(end_date="+30d", tzinfo=None),
            # updatedDate=fake.future_datetime(end_date="+30d", tzinfo=None),
        )
        author.make()
