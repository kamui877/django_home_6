from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            product = position['product']
            quantity = position['quantity']
            price = position['price']
            StockProduct.objects.create(stock=stock, product=product, quantity=quantity, price=price)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position in positions:
            product = position['product']
            quantity = position['quantity']
            price = position['price']
            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults={'quantity': quantity, 'price': price})
        return stock
