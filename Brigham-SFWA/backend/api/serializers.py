# from django.contrib.auth.models import User
# from rest_framework import serializers, fields

# from api.models import (
#     Equity_Security_Master,
#     Position,
#     Trade,
#     Live_Target_Portfolio,
#     Portfolio_ExAnte_Stats,
# )
# from django.db import models
# from django.utils import timezone


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "url",
#             "first_name",
#             "last_name",
#             "username",
#             "email",
#             "password",
#             "is_staff",
#         ]


# class ChangePasswordSerializer(serializers.Serializer):
#     model = User

#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)


# class EquitySecurityMasterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Equity_Security_Master
#         fields = "__all__"


# class PositionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Position
#         fields = [
#             "asset_id",
#             "ticker",
#             "num_of_shares",
#             "asset_type",
#             "price",
#             "position_value",
#             "date",
#         ]


# class TradeSerializer(serializers.ModelSerializer):
#     ticker = serializers.SerializerMethodField("get_ticker_from_equity_security_master")

#     class Meta:
#         model = Trade
#         fields = [
#             "trade_id",
#             "asset_id",
#             "ticker",
#             "trade_type",
#             "num_of_shares",
#             "price",
#             "tot_price",
#             "trade_status",
#             "trade_time",
#         ]

#     def get_ticker_from_equity_security_master(self, trd):
#         ticker = trd.asset.ticker
#         return ticker


# class LiveTargetPortfolioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Live_Target_Portfolio
#         fields = [
#             "asset",
#             "ticker",
#             "model_er",
#             "annualized_er",
#             "beta_to_b",
#             "alpha",
#             "oa_weight",
#             "b_weight",
#             "c_weight",
#             "backlog",
#             "backlog_risk",
#             "commit_time",
#             "commit_maker",
#             "is_latest",
#         ]


# class PortfolioExAnteStatsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Portfolio_ExAnte_Stats
#         fields = "__all__"
