from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import views_client, views_wishlist, views_product, views_reviewproduct, views_user

urlpatterns = [
    path('new_user/', views_user.create_user),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('client/', views_client.client_list),
    path('client/<pk>', views_client.client_detail),

    path('wishlist/', views_wishlist.wishlist_list),
    path('wishlist/<pk>', views_wishlist.wishlist_detail),

    path('product/', views_product.product_list),
    path('product/<pk>', views_product.product_detail),

    path('review/', views_reviewproduct.review_list),
    path('review/<pk>', views_reviewproduct.review_detail),
]
