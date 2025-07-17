
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('users.urls')),
    path('api/',include('listings.urls')),
    path('api/',include('inquiries.urls')),
   path('api/payments/', include('payments.urls')),
   path('api/', include('cart.urls')),

    # token authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_roots=settings.STATIC_ROOT)
