from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('', include('snippets.urls')),
]

# adding login to the browsable API
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
