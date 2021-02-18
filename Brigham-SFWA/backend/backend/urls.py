from django.urls import include, path
from rest_framework import routers
from api import views
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token


# router = routers.DefaultRouter()
# router.register(r"api/users", views.UserViewSet)
# router.register(r"api/positions", views.PositionViewSet)
# router.register(r"api/trades", views.TradeViewSet)
# router.register(r"api/securities", views.EquitySecurityMasterViewSet)

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    #     path("api/login/", obtain_auth_token),
    #     path("api/change-password/", views.ChangePasswordView.as_view(),),
    #     path("api/securities/r3000/", views.get_securities_r3000),
    #     path("api/positions/filter/date/", views.filter_positions_by_date),
    #     path("api/trades/filter/date/", views.filter_trades_by_date),
    #     path("api/live-target-portfolio/history/", views.get_live_target_portfolio_history),
    #     path("api/live-target-portfolio/latest/", views.get_live_target_portfolio_latest),
    #     path("api/live-target-portfolio/commit/", views.commit_live_target_portfolio),
    #     path("api/portfolio-stats/history/", views.get_portfolio_stats_history),
    #     path("api/portfolio-stats/latest/", views.get_portfolio_stats_latest),
    #     path("api/portfolio-stats/commit/", views.commit_portfolio_stats),
    #     path("", include(router.urls)),
]
