from rest_framework import serializers, validators
from rest_framework.validators import UniqueValidator
from django.db.models import Sum

from api.models import ApiUser, Store, Product, Order, Supply


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    password = serializers.CharField(min_length=6, max_length=20,
                                     write_only=True)
    role = serializers.ChoiceField(choices=ApiUser.ROLE_CHOICES)

    def update(self, instance, validated_data):
        if email := validated_data.get('email'):
            instance.email = email
            instance.save(update_fields=['email'])

        if password := validated_data.get('password'):
            instance.set_password(password)
            instance.save(update_fields=['password'])
        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])
        return user


class StoreSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Store
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class SupplyWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Supply
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class OrderWriteSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.filter(orders__isnull=True),
    #     validators=[
    #         validators.UniqueValidator(
    #             queryset=Order.objects.all(),
    #             message='This product is sold.'
    #         )
    #     ])

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}

    # def validate_quantity(self, value):
    #     """
    #     Check that the blog post is about Django.
    #     """
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError(
    #             "Blog post is not about Django")
    #     return value

    # def validate(self, data):
    #     """
    #     Check that start is before finish.
    #     """
    #     if data['start'] > data['finish']:
    #         raise serializers.ValidationError(
    #             "finish must occur after start")
    #     return data

    def validate(self, data):
        """
        Check that product is available in the store
        """
        supply_count = Supply.objects \
            .filter(product=data['product'], store=data['store']) \
            .aggregate(Sum('quantity', default=0))['quantity__sum']

        orders_count = Order.objects \
            .filter(product=data['product'], store=data['store']) \
            .aggregate(Sum('quantity', default=0))['quantity__sum']

        count = supply_count - orders_count

        if data['quantity'] > count:
            if count <= 0:
                error_msg = 'This item is not available in this store.'
            else:
                error_msg = f'There are only three {count} left in this store.'
            raise serializers.ValidationError(error_msg)
        return data

    # Book.objects.filter(publisher__name="BaloneyPress").count()

# class AvailabilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Availability
#         fields = '__all__'
#         extra_kwargs = {'id': {'read_only': True}}
