from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('paniavault/', include('paniavault.urls', namespace='paniavault')),
    path('vitrin/', include('vitrin.urls', namespace='vitrin')),
    path('meltvitrin/', include('meltvitrin.urls', namespace='meltvitrin')),
    path('finance/', include('finance.urls', namespace='finance')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('paniaplatform/', include('paniaplatform.urls', namespace='paniaplatform')),
    path('transfers/', include('transfers.urls', namespace='transfers')),
    path('select2/', include('django_select2.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)