from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.staticfiles import finders


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Cardamom", "Cardamom"),
        ("Clove", "Clove"),
        ("Cinnamon", "Cinnamon"),
        ("Pepper", "Black Pepper"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default="Other")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True, help_text="Direct image URL (e.g., Unsplash)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        name_slug = slugify(self.name or "")
        cat_slug = slugify(self.category or "")

        bases = set([
            name_slug,
            name_slug.replace('-', '_'),
            cat_slug,
            cat_slug.replace('-', '_'),
        ])

        # Add versions without separators (e.g., bayleaf)
        sep_less = set()
        for b in list(bases):
            compact = b.replace('-', '').replace('_', '')
            if compact:
                sep_less.add(compact)
        bases |= sep_less

        # Add first word of product name as a heuristic (e.g., garlic from "Garlic Clove")
        first_word = (self.name or "").strip().split(" ")[0].lower()
        if first_word:
            fw_slug = slugify(first_word)
            bases.add(fw_slug)
            bases.add(fw_slug.replace('-', '_'))

        # Common aliases to match existing filenames
        # e.g., 'clove' -> 'cloves', 'pepper' (category) -> 'black_pepper'
        alias_map = {
            'clove': ['cloves'],
            'pepper': ['black_pepper'],
            'black-pepper': ['black_pepper'],
        }
        expanded = set(bases)
        for base in list(bases):
            for alias in alias_map.get(base, []):
                expanded.add(alias)

        # Build candidate static paths by priority
        paths = []
        for b in expanded:
            # Prefer vector icons when available
            paths.append(f"images/{b}.svg")
        for b in expanded:
            paths.append(f"images/{b}.svg")
        for b in expanded:
            paths.append(f"images/{b}.png")
        for b in expanded:
            paths.append(f"images/{b}.jpg")
        for b in expanded:
            paths.append(f"images/{b}.jpeg")
        # Also try variants with spaces (e.g., "ground cardamom.png")
        space_variants = set()
        for b in expanded:
            s = b.replace('-', ' ').replace('_', ' ')
            if s:
                space_variants.add(s)
        for s in space_variants:
            paths.append(f"images/{s}.svg")
        for s in space_variants:
            paths.append(f"images/{s}.png")
        for s in space_variants:
            paths.append(f"images/{s}.jpg")
        for s in space_variants:
            paths.append(f"images/{s}.jpeg")

        for path in paths:
            if finders.find(path):
                return static(path)
        return static('images/.png')


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self) -> str:
        return self.question


class VisitorRegistration(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Message from {self.name}"


# --- E-commerce models ---
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    class Meta:
        ordering = ['-created_at']
    def __str__(self) -> str:
        return f"Order #{self.pk} - {self.name} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.product.name} x{self.quantity}"
