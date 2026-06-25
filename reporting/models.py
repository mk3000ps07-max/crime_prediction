from django.db import models
from django.contrib.auth.models import User
from records.models import CrimeRecord
import datetime

class Report(models.Model):
    """
    Store generated reports about crime statistics
    """
    REPORT_TYPES = [
        ('DAILY', 'Daily Report'),
        ('WEEKLY', 'Weekly Report'),
        ('MONTHLY', 'Monthly Report'),
        ('QUARTERLY', 'Quarterly Report'),
        ('YEARLY', 'Yearly Report'),
        ('CUSTOM', 'Custom Report'),
    ]

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports_created')
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    summary = models.TextField()
    total_incidents = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"{self.title} ({self.report_type})"


class ReportStatistic(models.Model):
    """
    Store detailed statistics for each report
    """
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='statistics')
    total_crimes = models.IntegerField(default=0)
    total_thefts = models.IntegerField(default=0)
    total_assaults = models.IntegerField(default=0)
    total_vandalism = models.IntegerField(default=0)
    total_robbery = models.IntegerField(default=0)
    total_other = models.IntegerField(default=0)
    highest_crime_hour = models.IntegerField(null=True, blank=True)
    most_affected_area = models.CharField(max_length=255, blank=True)
    average_incidents_per_day = models.FloatField(default=0.0)
    day_with_most_incidents = models.CharField(max_length=20, blank=True)  # e.g., 'Monday', 'Tuesday'

    class Meta:
        verbose_name_plural = "Report Statistics"

    def __str__(self):
        return f"Statistics for {self.report.title}"


class ReportDistribution(models.Model):
    """
    Track who receives reports and how
    """
    DISTRIBUTION_METHODS = [
        ('EMAIL', 'Email'),
        ('DOWNLOAD', 'Download'),
        ('PRINT', 'Print'),
        ('DASHBOARD', 'Dashboard View'),
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='distributions')
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_reports')
    distribution_method = models.CharField(max_length=50, choices=DISTRIBUTION_METHODS)
    distributed_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Report Distributions"

    def __str__(self):
        return f"{self.report.title} -> {self.recipient.username} ({self.distribution_method})"


class ExportLog(models.Model):
    """
    Track all data exports for audit purposes
    """
    EXPORT_FORMATS = [
        ('CSV', 'CSV'),
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('JSON', 'JSON'),
    ]

    exported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='export_logs')
    export_format = models.CharField(max_length=20, choices=EXPORT_FORMATS)
    export_date = models.DateTimeField(auto_now_add=True)
    record_count = models.IntegerField()
    filters_applied = models.CharField(max_length=500, blank=True)  # JSON string of filters
    file_size = models.IntegerField(null=True, blank=True)  # in bytes
    download_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-export_date']
        verbose_name_plural = "Export Logs"

    def __str__(self):
        return f"{self.export_format} export by {self.exported_by.username} on {self.export_date.date()}"
