from rest_framework import serializers
from . import models


IMAGE_ERRORS = {
    'required': 'Загрузите изображение',
    'invalid': 'Загрузите изображение',
    'invalid_image': 'Загрузите изображение',
    'empty': 'Загрузите изображение',
}


class ListingSerializer(serializers.ModelSerializer):
    # на вход — файл в поле image, на выход — полный адрес в поле image_url
    image_url = serializers.ImageField(source='image', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Listing
        fields = ['id', 'title', 'description', 'price', 'image', 'image_url', 'created_at', 'is_mine']
        extra_kwargs = {
            "title": {
                "error_messages": {
                    'required': 'Введите название',
                    'blank': 'Введите название',
                    'max_length': 'Максимум 80 символов',
                },
            },
            "description": {
                "error_messages": {'max_length': 'Максимум 500 символов'},
            },
            "price": {
                # "validators": [MinValueValidator(1)],
                "min_value": 1,
                "error_messages": {
                    'required': 'Цена должна быть числом',
                    'invalid': 'Цена должна быть числом',
                    'min_value': 'Цена должна быть больше 0',
                },
            },
            "image": {
                "write_only": True,
                "error_messages": IMAGE_ERRORS,
            },
        }

    def get_is_mine(self, obj):
        req = self.context.get('request')
        return req is not None and obj.owner_id == req.user.id

    def validate_image(self, image):
        if image.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Максимум 5 МБ')

        return image
