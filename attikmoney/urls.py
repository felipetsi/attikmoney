from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('attikmoney.accounts.urls')),
    path('accounts/', include('attikmoney.accounts.urls', namespace='accounts')),
    path('dashboard/', include('attikmoney.dashboard.urls', namespace='dashboard')),
    path('core/', include('attikmoney.core.urls', namespace='core')),
    path('report/', include('attikmoney.report.urls', namespace='report')),
]

#==================================================
# Now, add the below line in the bottom of Url file
# import file or You can directly paste the contents of execute.py
#==================================================
from attikmoney.scheduler import execute

#==================================================