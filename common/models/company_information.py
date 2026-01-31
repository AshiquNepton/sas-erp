from django.db import models


class Organization(models.Model):
    BUSINESS_TYPES = (
        (1, 'Laundry'),
        (2, 'Restaurant'),
    )

    CompanyId = models.IntegerField(primary_key=True)

    CompanyName = models.CharField(max_length=300)
    ArabicName = models.CharField(max_length=300, null=True, blank=True)
    Subtitle = models.CharField(max_length=300, null=True, blank=True)

    Address1 = models.CharField(max_length=300, null=True, blank=True)
    Address2 = models.CharField(max_length=300, null=True, blank=True)
    Address3 = models.CharField(max_length=300, null=True, blank=True)

    Phone = models.CharField(max_length=300, null=True, blank=True)
    Mobile = models.CharField(max_length=300, null=True, blank=True)
    Url = models.CharField(max_length=300, null=True, blank=True)
    Email = models.EmailField(null=True, blank=True)

    TinNo = models.CharField(max_length=300, null=True, blank=True)
    CrNo = models.CharField(max_length=300, null=True, blank=True)
    LicenseNo = models.CharField(max_length=300, null=True, blank=True)

    BuildingNo = models.CharField(max_length=300, null=True, blank=True)
    StreetName = models.CharField(max_length=300, null=True, blank=True)
    Zone = models.CharField(max_length=300, null=True, blank=True)
    Area = models.CharField(max_length=300, null=True, blank=True)
    City = models.CharField(max_length=300, null=True, blank=True)
    State = models.CharField(max_length=300, null=True, blank=True)
    District = models.CharField(max_length=300, null=True, blank=True)
    PoBox = models.CharField(max_length=300, null=True, blank=True)

    PlotIdentification = models.CharField(max_length=300, null=True, blank=True)

    AccountNumber = models.CharField(max_length=300, null=True, blank=True)
    AccountName = models.CharField(max_length=300, null=True, blank=True)
    Branch = models.CharField(max_length=300, null=True, blank=True)
    Ifsc = models.CharField(max_length=300, null=True, blank=True)

    PayerId = models.CharField(max_length=300, null=True, blank=True)
    PayerBank = models.CharField(max_length=300, null=True, blank=True)
    PayerIban = models.CharField(max_length=300, null=True, blank=True)

    PeriodFrom = models.DateField()
    PeriodTo = models.DateField()

    DefaultDb = models.SmallIntegerField(null=True, blank=True)
    BusinessType = models.SmallIntegerField(choices=BUSINESS_TYPES)

    CreatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Organization'
        ordering = ['-CreatedAt']

    def __str__(self):
        return f"{self.CompanyName}"
