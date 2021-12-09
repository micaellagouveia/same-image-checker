from django.urls import path
from images_checker import views

urlpatterns = [
    path('check-image/', views.check_image, name='check-image'),
    path('property/<int:property_id>/add-image/', views.add_image, name='add-image'),
    path('property/<int:property_id>/add-image-bucket/', views.add_image_bucket_by_property, name='add-image-bucket-by-property'),
    path('companies/<int:company_id>/add-all-images-bucket/', views.add_all_images_bucket, name='add-all-images-bucket'),
]