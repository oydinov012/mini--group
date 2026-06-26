from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.user_app import (
    RegisterView, LogoutView, LoginView,
    ForgotPasswordView, PasswordResetConfirmView,
    UserProfileView, UpdatePasswordView,
)
from api.views.shop_app import (
    CategoryListCreateView, CategoryDetailView,
    BrandsListCreateView, BrandsDetailView,
    ProductListCreateView, ProductDetailView, ProductCompareView,
    WishlistListView, WishlistAddView, WishlistDeleteView,
    ReviewListView, ReviewCreateView, ReviewDetailView,
    ReviewAdminListView, ReviewAdminDetailView, ReviewPublishView,
    CartView, CartItemAddView, CartItemUpdateView, CartItemDeleteView, CartClearView,
    SaleListCreateView, SaleDetailView,
    DeliveryAddressListCreateView, DeliveryAddressDetailView, DeliveryAddressSetDefaultView,
    HomePageView,
)
from api.views.order_app import (
    PromoCodeListCreateView, PromoCodeDetailView, PromoCodeCheckView,
    OrderListCreateView, OrderDetailView, OrderStatusUpdateView,
    OrderItemListCreateView, OrderItemDetailView,
)
from api.views.news_app import (
    NewsView, NewsTypeView,
    NewsAdminListCreateView, NewsAdminDetailView,
    NewsTypeAdminListCreateView, NewsTypeAdminDetailView,
    NewsImageAdminListCreateView, NewsImageAdminDetailView,
)

r = DefaultRouter()
r.register(r'news-type', NewsTypeView, basename='news-type')
r.register(r'news', NewsView, basename='news')

urlpatterns = [
    # ── Home page ────────────────────────────────────────────────────────────
    path('home/', HomePageView.as_view(), name='home_page'),

    # ── Auth ─────────────────────────────────────────────────────────────────
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/', PasswordResetConfirmView.as_view(), name='reset_password'),

    # ── Profile ───────────────────────────────────────────────────────────────
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/change-password/', UpdatePasswordView.as_view(), name='change_password'),

    # ── Shop ─────────────────────────────────────────────────────────────────
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('brands/', BrandsListCreateView.as_view(), name='brands_list_create'),
    path('brands/<int:pk>/', BrandsDetailView.as_view(), name='brands_detail'),

    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/compare/', ProductCompareView.as_view(), name='product_compare'),   # ← avval
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),    # ← keyin

    # ── Wishlist ──────────────────────────────────────────────────────────────
    path('wishlist/', WishlistListView.as_view(), name='wishlist_list'),
    path('wishlist/add/', WishlistAddView.as_view(), name='wishlist_add'),
    path('wishlist/<int:pk>/', WishlistDeleteView.as_view(), name='wishlist_delete'),

    # ── Review (foydalanuvchi) ────────────────────────────────────────────────
    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),

    # ── Review (admin) ────────────────────────────────────────────────────────
    path('admin/reviews/', ReviewAdminListView.as_view(), name='admin_review_list'),
    path('admin/reviews/<int:pk>/', ReviewAdminDetailView.as_view(), name='admin_review_detail'),
    path('admin/reviews/<int:pk>/publish/', ReviewPublishView.as_view(), name='admin_review_publish'),

    # ── Cart ──────────────────────────────────────────────────────────────────
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', CartItemAddView.as_view(), name='cart_item_add'),
    path('cart/clear/', CartClearView.as_view(), name='cart_clear'),
    path('cart/items/<int:pk>/', CartItemUpdateView.as_view(), name='cart_item_update'),
    path('cart/items/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart_item_delete'),

    # ── Sales (Aksiya) ────────────────────────────────────────────────────────
    path('sales/', SaleListCreateView.as_view(), name='sale_list_create'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale_detail'),

    # ── Delivery addresses ────────────────────────────────────────────────────
    path('addresses/', DeliveryAddressListCreateView.as_view(), name='address_list_create'),
    path('addresses/<int:pk>/', DeliveryAddressDetailView.as_view(), name='address_detail'),
    path('addresses/<int:pk>/default/', DeliveryAddressSetDefaultView.as_view(), name='address_set_default'),

    # ── Promo ─────────────────────────────────────────────────────────────────
    path('promo/', PromoCodeListCreateView.as_view(), name='promo_list_create'),
    path('promo/check/', PromoCodeCheckView.as_view(), name='promo_check'),
    path('promo/<int:pk>/', PromoCodeDetailView.as_view(), name='promo_detail'),

    # ── Orders ────────────────────────────────────────────────────────────────
    path('orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('orders/<int:order_id>/items/', OrderItemListCreateView.as_view(), name='orderitem_list_create'),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='orderitem_detail'),

    # ── News ──────────────────────────────────────────────────────────────────
    path('news/', include(r.urls)),

    # ── News Admin CRUD ───────────────────────────────────────────────────────
    path('admin/news/', NewsAdminListCreateView.as_view(), name='admin_news_list_create'),
    path('admin/news/<int:pk>/', NewsAdminDetailView.as_view(), name='admin_news_detail'),
    path('admin/news-types/', NewsTypeAdminListCreateView.as_view(), name='admin_newstype_list_create'),
    path('admin/news-types/<int:pk>/', NewsTypeAdminDetailView.as_view(), name='admin_newstype_detail'),
    path('admin/news/<int:news_id>/images/', NewsImageAdminListCreateView.as_view(), name='admin_newsimage_list_create'),
    path('admin/news-images/<int:pk>/', NewsImageAdminDetailView.as_view(), name='admin_newsimage_detail'),
]