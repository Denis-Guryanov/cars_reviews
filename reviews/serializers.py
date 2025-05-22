from rest_framework import serializers
from .models import Country, Manufacturer, Car, Comment

class CountrySerializer(serializers.ModelSerializer):
    manufacturers = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'name', 'manufacturers']

    def get_manufacturers(self, obj):
        return list(obj.manufacturer_set.values('id', 'name'))

class ManufacturerSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True,
        help_text="ID существующей страны"
    )
    cars = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'country_id', 'cars', 'comment_count']

    def get_cars(self, obj):
        return list(obj.car_set.values('id', 'name'))

    def get_comment_count(self, obj):
        return Comment.objects.filter(car__manufacturer=obj).count()

class CarSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(),
        source='manufacturer',
        write_only=True,
        help_text="ID существующего производителя"
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacturer', 'manufacturer_id', 'start_year', 'end_year', 'comments']

    def get_comments(self, obj):
        return list(obj.comment_set.values('email', 'text', 'created_at'))

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'email', 'car', 'created_at', 'text']
        read_only_fields = ['created_at']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email обязателен.")
        return value

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Комментарий должен содержать минимум 10 символов.")
        return value