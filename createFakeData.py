import uuid

import django
django.setup()

from model_bakery.recipe import Recipe
from shop.models import Shop, ShopImage
from faker import Faker

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

# for i in ShopProduct.objects.all():
#     i.id = None
#     i.save()

for i in Shop.objects.all():
    for k in range(4):
        author = Recipe(
            ShopImage,
            shop=i,
            # product=Product.objects.order_by('?').first(),
            # user=User.objects.order_by('?').first(),
            # category=Category.objects.order_by('?').first(),
            # class_id=ClassId.objects.order_by('?').first(),
            # unit=ProductUnit.objects.order_by('?').first(),
            # parent=fake.text(),
            # parent=ArticleEncyclopediaCategory.objects.order_by("?").first(),
            image=images[k],
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
