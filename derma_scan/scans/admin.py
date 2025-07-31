from django.contrib import admin

from .models import (
    Diagnosis, 
    SkinImage, 
    ProductRecommendation
)


@admin.register(SkinImage)
class SkinImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body_part', 'uploaded_at', 'is_analyzed')
    list_filter = ('body_part', 'is_analyzed', 'uploaded_at')
    search_fields = ('user__username', 'body_part')
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'label', 'confidence', 'created_at')
    search_fields = ('label', 'description', 'user__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'ai_response')


@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'diagnosis', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'reason', 'diagnosis__result')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

