from django.contrib import admin
from django.urls import include, path
from gcpdjango.apps.main import urls as main_urls
from gcpdjango.apps.base import urls as base_urls
from gcpdjango.apps.users import urls as user_urls

# Customize admin title, headers
admin.site.site_header = "gcp-django-stanford Administration"
admin.site.site_title = "gcp-django-stanford Admin"
admin.site.index_title = "gcp-django-stanford administration"

# Configure custom error pages
handler404 = "gcpdjango.apps.base.views.handler404"
handler500 = "gcpdjango.apps.base.views.handler500"

urlpatterns = [
    path("", include(base_urls)),
    path("", include(main_urls)),
    path("", include(user_urls)),
    path("admin/", admin.site.urls),
]
