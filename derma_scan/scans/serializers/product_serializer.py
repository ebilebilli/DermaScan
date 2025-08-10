from rest_framework import serializers

from scans.models import ProductRecommendation


class ProductRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRecommendation
        fields = '__all__'
