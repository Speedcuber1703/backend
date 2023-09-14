from pytils.translit import slugify
from PIL import Image, ImageOps

def unique_slugify(instance, slug) -> str:
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG
    """
    model = instance.__class__
    unique_slug = instance.slug
    if not instance.slug or model.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
        unique_slug = slugify(slug)
        count = 2
        while model.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
            unique_slug = f'{unique_slug}-{count}'
            count += 1
    return unique_slug


def get_client_ip(request):
    """
    Получение IP пользователя
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip


def image_compress(image_path, height, width):
    """
    Оптимизация изображений
    """

    img = Image.open(image_path)

    if img.mode != 'RGB':
        img.convert('RGB')

    if img.height > height or img.width > width:
        output_size = (height, width)
        img.thumbnail(output_size)

    img = ImageOps.exif_transpose(img)
    img.save(image_path, format='JPEG', quality=90, optimize=True)

    