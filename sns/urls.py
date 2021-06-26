from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # mediaを使うために追加
from . import settings  # mediaを使うために追加
from accounts.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('microposts/', include('microposts.urls')), # 追加
    path('', HomeView.as_view(), name='home')
]

# mediaを使うために追加
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)