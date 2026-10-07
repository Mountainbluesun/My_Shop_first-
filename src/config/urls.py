
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from store.views import index, stripe_webhook

from config import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('boutique/', include('store.urls')),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
