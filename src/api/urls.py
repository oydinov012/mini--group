from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.user_app import RegisterView, LogoutView, LoginView ,ForgotPasswordView, PasswordResetConfirmView
from api.views.shop_app import (
    CategoryListCreateView, CategoryDetailView,
    BrandsListCreateView, BrandsDetailView,
    ProductListCreateView, ProductDetailView,
    WishlistListView, WishlistAddView, WishlistDeleteView,
    ReviewListView, ReviewCreateView, ReviewDetailView,
)
from api.views.order_app import (
    PromoCodeListCreateView, PromoCodeDetailView, PromoCodeCheckView,
    OrderListCreateView, OrderDetailView, OrderStatusUpdateView,
    OrderItemListCreateView, OrderItemDetailView,
)

urlpatterns = [
    # auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/forgot-password/', ForgotPasswordView.as_view()),
    path('auth/reset-password/', PasswordResetConfirmView.as_view()),



    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('brands/', BrandsListCreateView.as_view(), name='brands_list_create'),
    path('brands/<int:pk>/', BrandsDetailView.as_view(), name='brands_detail'),

    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('wishlist/', WishlistListView.as_view(), name='wishlist_list'),
    path('wishlist/add/', WishlistAddView.as_view(), name='wishlist_add'),
    path('wishlist/<int:pk>/', WishlistDeleteView.as_view(), name='wishlist_delete'),

    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),

    path('promo/', PromoCodeListCreateView.as_view(), name='promo_list_create'),
    path('promo/<int:pk>/', PromoCodeDetailView.as_view(), name='promo_detail'),
    path('promo/check/', PromoCodeCheckView.as_view(), name='promo_check'),

    path('orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order_status_update'),

    path('orders/<int:order_id>/items/', OrderItemListCreateView.as_view(), name='orderitem_list_create'),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='orderitem_detail'),
]
