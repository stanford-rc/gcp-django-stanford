
from django.views.generic.base import TemplateView
from django.conf.urls import url
import gcpdjango.apps.base.views as views

urlpatterns = [
    url(r"^$", views.index_view, name="index"),
    url(r"^about/?$", views.about_view, name="about"),
    url(r"^contact/?$", views.contact_view, name="contact"),
    url(r"^terms/?$", views.terms_view, name="terms"),
    url(r"^privacy-policy/?$", views.terms_view, name="privacy-policy"),
    url(r"^search/?$", views.search_view, name="search"),
    url(r"^searching/?$", views.run_search, name="running_search"),
    url(r"^search/(?P<query>.+?)/?$", views.search_view, name="search_query"),
    url(
        r"^robots\.txt/$",
        TemplateView.as_view(
            template_name="base/robots.txt", content_type="text/plain"
        ),
    ),
]
