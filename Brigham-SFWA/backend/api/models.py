from django.db import models
from django.utils import timezone
from datetime import datetime


class Equity_Security_Master(models.Model):
    class Meta:
        verbose_name_plural = "equity security master"

    asset_id = models.CharField(
        verbose_name="asset id",
        max_length=40,
        null=False,
        blank=False,
        default="needs_id",
        primary_key=True,
    )
    ticker = models.CharField(
        verbose_name="ticker", max_length=40, null=True, blank=True
    )
    comnam = models.CharField(
        verbose_name="Company Name", max_length=40, null=True, blank=True
    )
    conid = models.CharField(verbose_name="conid", max_length=40, null=True, blank=True)
    cusip = models.CharField(verbose_name="cusip", max_length=40, null=True, blank=True)
    isin = models.CharField(verbose_name="isin", max_length=40, null=True, blank=True)
    valid_date = models.DateField(default=timezone.now)
    siccd = models.CharField(
        verbose_name="industry code", max_length=40, null=True, blank=True
    )
    country_code = models.CharField(
        verbose_name="country code", max_length=40, null=True, blank=True
    )
    prim_exch = models.CharField(
        verbose_name="prim exch", max_length=40, null=True, blank=True
    )
    currency = models.CharField(
        verbose_name="currency", max_length=40, null=True, blank=True
    )
    bnchmrk = models.CharField(
        verbose_name="benchmark", max_length=40, null=True, blank=True
    )

    def __str__(self):
        return self.asset_id


class Position(models.Model):
    asset = models.OneToOneField(
        Equity_Security_Master,
        related_name="positions",
        on_delete=models.PROTECT,
        verbose_name="asset id",
        primary_key=True,
    )
    ticker = models.CharField(
        verbose_name="ticker", max_length=40, null=True, blank=True
    )
    num_of_shares = models.IntegerField(
        verbose_name="num of shares", null=True, blank=True
    )
    asset_type = models.CharField(
        verbose_name="asset type", max_length=40, null=True, blank=True
    )
    price = models.FloatField(verbose_name="price", null=True, blank=True)
    position_value = models.FloatField(
        verbose_name="position value", null=True, blank=True
    )
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.ticker


class Trade(models.Model):
    trade_id = models.CharField(
        verbose_name="trade id",
        max_length=40,
        null=False,
        blank=False,
        primary_key=True,
    )
    asset = models.OneToOneField(
        Equity_Security_Master,
        related_name="trades",
        on_delete=models.PROTECT,
        verbose_name="asset id",
    )
    trade_type = models.CharField(
        verbose_name="trade type", max_length=40, null=True, blank=True
    )
    num_of_shares = models.IntegerField(
        verbose_name="num of shares", null=True, blank=True
    )
    price = models.FloatField(verbose_name="price", null=True, blank=True)
    tot_price = models.FloatField(verbose_name="tot price", null=True, blank=True)
    trade_status = models.CharField(
        verbose_name="status", max_length=40, null=True, blank=True
    )
    trade_time = models.CharField(
        verbose_name="date time", max_length=40, null=True, blank=True
    )

    def __str__(self):
        return self.trade_id


class Live_Target_Portfolio(models.Model):
    class Meta:
        verbose_name_plural = "live target portfolio"

    asset = models.ForeignKey(
        Equity_Security_Master,
        related_name="live_target_portfolio",
        on_delete=models.PROTECT,
        verbose_name="asset id",
        null=True,
        blank=True,
    )
    ticker = models.CharField(max_length=40)
    model_er = models.FloatField(verbose_name="model expected return")
    annualized_er = models.FloatField(verbose_name="annualized expected return")
    beta_to_b = models.FloatField(verbose_name="beta to benchmark")
    alpha = models.FloatField()
    oa_weight = models.FloatField(verbose_name="optimal active weight")
    b_weight = models.FloatField(verbose_name="weight in benchmark")
    c_weight = models.FloatField(verbose_name="current weight")
    backlog = models.FloatField()
    backlog_risk = models.FloatField()
    commit_maker = models.CharField(
        max_length=40, null=True, blank=True, default="anonymous"
    )
    is_latest = models.BooleanField(default=False)
    commit_time = models.CharField(
        default=datetime.now().strftime("%Y-%m-%d@%H:%M:%S"),
        max_length=40,
        editable=False,
    )

    def __str__(self):
        return self.ticker


class Portfolio_ExAnte_Stats(models.Model):
    class Meta:
        verbose_name_plural = "portfolio ex-ante stats"

    expected_return = models.FloatField(null=True, blank=True)
    beta_to_b = models.FloatField(
        verbose_name="beta to benchmark", null=True, blank=True
    )
    alpha_to_b = models.FloatField(
        verbose_name="alpha to benchmark", null=True, blank=True
    )
    info_ratio = models.FloatField(
        verbose_name="informational ratio", null=True, blank=True
    )
    commit_maker = models.CharField(
        max_length=40, null=True, blank=True, default="anonymous"
    )
    is_latest = models.BooleanField(default=True)
    commit_time = models.CharField(
        default=datetime.now().strftime("%Y-%m-%d@%H:%M:%S"),
        max_length=40,
        editable=False,
    )

    def __str__(self):
        return self.commit_maker + "'s commit on " + self.commit_time

