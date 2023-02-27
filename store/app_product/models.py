from django.db import models


class SaleProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    started_sale = models.DateField()
    finished_sale = models.DateField()


class Product(models.Model):
    DELIVERY = [
        ('f', 'free'),
        ('p', 'paid')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    archived = models.BooleanField(default=False)
    delivery = models.CharField(max_length=1, choices=DELIVERY)
    discount = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='product_image')


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=36, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(null=True, blank=True)
    review = models.CharField(max_length=200)

    def create(self, product: Product, name: str, rate: int, review: str):
        Comment.objects.create(product=product, name=name, rate=rate, review=review)

    def get_review_product(self, product: Product):
        return Comment.objects.filter(product=product)

    def get_count(self, product: Product):
        return Comment.objects.filter(product=product).count()
