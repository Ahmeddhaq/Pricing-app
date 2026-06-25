from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("history/", views.history_view, name="history_view"),
    path("invite/", views.invite_people, name="invite_people"),
    path("products/", views.products_list, name="products_list"),
    path("pricing/", views.pricing_list, name="pricing_list"),
    path("export/", views.export_dashboard, name="export_dashboard"),
    path("import/", views.import_upload, name="import_upload"),
    path("import/<int:import_id>/", views.import_detail, name="import_detail"),
    path("import/apply/<int:import_id>/", views.import_apply, name="import_apply"),
    path("quotation/create/", views.create_quotation, name="create_quotation"),
    path("api/notifications/", views.get_notifications, name="get_notifications"),
    path("api/notifications/read/", views.mark_notifications_read, name="mark_notifications_read"),
    path("inquiry/send/", views.send_inquiry, name="send_inquiry"),
    path("crm/", views.crm_dashboard, name="crm_dashboard"),
    path("crm/lead/create/", views.crm_lead_create, name="crm_lead_create"),
    path("crm/lead/<int:pk>/update/", views.crm_lead_update, name="crm_lead_update"),
    path("crm/lead/<int:pk>/edit/", views.crm_lead_edit, name="crm_lead_edit"),
    path("crm/lead/<int:pk>/delete/", views.crm_lead_delete, name="crm_lead_delete"),
]
