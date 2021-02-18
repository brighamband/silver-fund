# import datetime
# from time import strftime

# from django.contrib.auth.models import User
# from django.shortcuts import render
# from rest_framework import generics, permissions, status, viewsets
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.renderers import JSONRenderer
# from rest_framework.response import Response

# from api.models import (
#     Equity_Security_Master,
#     Live_Target_Portfolio,
#     Portfolio_ExAnte_Stats,
#     Position,
#     Trade,
# )
# from api.serializers import *


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """

#     queryset = User.objects.all().order_by("-date_joined")
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """

#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self, queryset=None):
#         name_user = self.request.data.get("user")
#         obj = User.objects.get(username=name_user)
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response(
#                     {"old_password": ["Wrong password."]},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 "status": "success",
#                 "code": status.HTTP_200_OK,
#                 "message": "Password updated successfully",
#                 "data": [],
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PositionViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows positions to be viewed or edited.
#     """

#     queryset = Position.objects.order_by("-date", "ticker")
#     serializer_class = PositionSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class TradeViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows trades to be viewed or edited.
#     """

#     queryset = Trade.objects.order_by("-trade_time", "asset_id")
#     serializer_class = TradeSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class EquitySecurityMasterViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows securities to be viewed or edited.
#     """

#     # FIXME at some point we need to set this up to filter to most recent date
#     queryset = Equity_Security_Master.objects.order_by("ticker")
#     serializer_class = EquitySecurityMasterSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# @api_view(["GET"])
# def get_securities_r3000(request):
#     """
#     API endpoint that allows all Russell 3000 securities to be viewed.
#     """
#     r3000_securities = Equity_Security_Master.objects.filter(
#         bnchmrk="Russell_3000"
#     ).order_by("ticker")
#     serializer = EquitySecurityMasterSerializer(r3000_securities, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def filter_positions_by_date(request):
#     """
#     API endpoint that returns all positions on a single date or date range specified.
#     """
#     start_date = request.query_params.get("start")
#     end_date = request.query_params.get("end")
#     if end_date is None:
#         end_date = start_date
#     positions = Position.objects.filter(date__range=(start_date, end_date)).order_by(
#         "-date", "ticker"
#     )
#     serializer = PositionSerializer(positions, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def filter_trades_by_date(request):
#     start_date = request.query_params.get("start")
#     end_date = request.query_params.get("end")
#     trades = Trade.objects.filter(trade_time__range=(start_date, end_date)).order_by(
#         "-trade_time", "asset_id"
#     )
#     serializer = TradeSerializer(trades, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def get_live_target_portfolio_history(request):
#     """
#     API endpoint that allows full history (latest->oldest) of live target portfolio to be viewed.
#     """
#     all_target = Live_Target_Portfolio.objects.order_by("-is_latest", "-commit_time")
#     serializer = LiveTargetPortfolioSerializer(all_target, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def get_live_target_portfolio_latest(request):
#     """
#     API endpoint that allows latest live target portfolio commit to be viewed.
#     """
#     latest_target = Live_Target_Portfolio.objects.filter(is_latest=True).order_by(
#         "-commit_time"
#     )
#     serializer = LiveTargetPortfolioSerializer(latest_target, many=True)
#     return Response(serializer.data)


# @api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
# def commit_live_target_portfolio(request):
#     """
#     API endpoint that commits paper target portfolio as the live active portfolio.
#     """
#     serializer = LiveTargetPortfolioSerializer(data=request.data, many=True)
#     if serializer.is_valid():
#         Live_Target_Portfolio.objects.all().update(is_latest=False)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def get_portfolio_stats_history(request):
#     """
#     API endpoint that allows the full history (latest->oldest) of Portfolio Ex-Ante Stats to be viewed.
#     """
#     all_stats = Portfolio_ExAnte_Stats.objects.order_by("-is_latest", "-commit_time")
#     serializer = PortfolioExAnteStatsSerializer(all_stats, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def get_portfolio_stats_latest(request):
#     """
#     API endpoint that allows the latest Portfolio Ex-Ante Stats to be viewed.
#     """
#     latest_stats = Portfolio_ExAnte_Stats.objects.get(is_latest=True)
#     serializer = PortfolioExAnteStatsSerializer(latest_stats)
#     return Response(serializer.data)


# @api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
# def commit_portfolio_stats(request):
#     """
#     API endpoint that commits paper target portfolio as the live active portfolio.
#     """
#     serializer = PortfolioExAnteStatsSerializer(data=request.data)
#     if serializer.is_valid():
#         Portfolio_ExAnte_Stats.objects.all().update(is_latest=False)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
