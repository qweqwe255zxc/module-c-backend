from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from listings.models import Listing

User = get_user_model()
IMAGES_DIR = settings.BASE_DIR / 'seed_images'

LISTINGS = [
    # (название, описание, цена, чьё, сколько дней назад создано)
    ('Велосипед Stels Navigator', 'Горный велосипед, 21 скорость', 14500, 'seller', 1),
    ('Кресло офисное', 'Сетчатая спинка, регулировка высоты', 6200, 'seller', 2),
    ('iPhone 12 128 Gb', 'Батарея 87%, полный комплект', 32000, 'buyer', 3),
    ('Настольная лампа', '', 900, 'seller', 4),
    ('Гитара Yamaha F310', 'Акустическая, с чехлом', 11000, 'buyer', 5),
    ('Книжный шкаф', 'Дуб, высота 180 см', 4500, 'seller', 7),
]


class Command(BaseCommand):
    help = 'Пересоздаёт тестовых пользователей и объявления'

    def handle(self, *args, **options):
        # 1. очистка
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # 2. пользователи
        users = {
            'seller': User.objects.create_user(email='seller@example.com', password='secret123'),
            'buyer': User.objects.create_user(email='buyer@example.com', password='secret123'),
        }

        # только картинки, без служебных файлов вроде .DS_Store
        images = [p for p in sorted(IMAGES_DIR.iterdir()) if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.svg')]

        # 3–5. объявления
        for i, (title, description, price, owner, days_ago) in enumerate(LISTINGS):
            listing = Listing(owner=users[owner], title=title, description=description, price=price)

            image_path = images[i % len(images)]          # картинки по кругу
            with open(image_path, 'rb') as f:
                listing.image.save(image_path.name, File(f))   # копирует файл в media и сохраняет объявление

            Listing.objects.filter(pk=listing.pk).update(
                created_at=timezone.now() - timedelta(days=days_ago)
            )

        self.stdout.write(f'Готово: {len(users)} пользователя, {len(LISTINGS)} объявлений')
