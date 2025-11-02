"""
Data models for university dashboard.
Following the common-modules.md and database.md specifications.
Implements all 5 data models as defined in the database schema.
"""
from django.db import models
from django.conf import settings


class DepartmentKPI(models.Model):
    """
    Department Key Performance Indicators data model.
    Stores annual performance metrics for each department.
    """
    year = models.IntegerField(
        help_text="Evaluation year"
    )
    college = models.CharField(
        max_length=100,
        help_text="College name"
    )
    department = models.CharField(
        max_length=100,
        help_text="Department name"
    )
    employment_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Employment rate (%)"
    )
    full_time_faculty = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of full-time faculty members"
    )
    visiting_faculty = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of visiting faculty members"
    )
    tech_transfer_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Technology transfer revenue (hundred million won)"
    )
    intl_conference_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of international conferences"
    )

    class Meta:
        db_table = 'department_kpis'
        unique_together = [['year', 'college', 'department']]
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['department']),
        ]
        ordering = ['-year', 'college', 'department']

    def __str__(self):
        return f"{self.college} - {self.department} ({self.year})"


class Publication(models.Model):
    """
    Publication (paper) data model.
    Stores information about academic publications.
    """
    publication_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique publication ID"
    )
    publication_date = models.DateField(
        help_text="Publication date"
    )
    college = models.CharField(
        max_length=100,
        help_text="College name"
    )
    department = models.CharField(
        max_length=100,
        help_text="Department name"
    )
    title = models.TextField(
        help_text="Publication title"
    )
    primary_author = models.CharField(
        max_length=100,
        help_text="Primary author name"
    )
    co_authors = models.TextField(
        null=True,
        blank=True,
        help_text="Co-authors (semicolon-separated)"
    )
    journal_name = models.CharField(
        max_length=255,
        help_text="Journal name"
    )
    journal_grade = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Journal grade/tier"
    )
    impact_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Impact factor"
    )
    is_project_linked = models.BooleanField(
        default=False,
        help_text="Whether linked to research project"
    )

    class Meta:
        db_table = 'publications'
        indexes = [
            models.Index(fields=['publication_date']),
            models.Index(fields=['journal_grade']),
        ]
        ordering = ['-publication_date']

    def __str__(self):
        return f"{self.title} ({self.publication_date.year})"


class Student(models.Model):
    """
    Student data model.
    Stores student information.
    """
    PROGRAM_CHOICES = [
        ('학사', '학사'),
        ('석사', '석사'),
        ('박사', '박사'),
    ]

    ENROLLMENT_CHOICES = [
        ('재학', '재학'),
        ('휴학', '휴학'),
        ('졸업', '졸업'),
        ('자퇴', '자퇴'),
        ('제적', '제적'),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Student ID"
    )
    name = models.CharField(
        max_length=100,
        help_text="Student name"
    )
    college = models.CharField(
        max_length=100,
        help_text="College name"
    )
    department = models.CharField(
        max_length=100,
        help_text="Department name"
    )
    grade = models.IntegerField(
        null=True,
        blank=True,
        help_text="Grade (0 for graduate school)"
    )
    program_type = models.CharField(
        max_length=50,
        choices=PROGRAM_CHOICES,
        help_text="Program type"
    )
    enrollment_status = models.CharField(
        max_length=50,
        choices=ENROLLMENT_CHOICES,
        help_text="Enrollment status"
    )
    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Gender"
    )
    admission_year = models.IntegerField(
        help_text="Admission year"
    )
    advisor = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Advisor name"
    )
    email = models.EmailField(
        null=True,
        blank=True,
        help_text="Email address"
    )

    class Meta:
        db_table = 'students'
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['enrollment_status']),
        ]
        ordering = ['student_id']

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class ResearchBudgetData(models.Model):
    """
    Research budget data model (denormalized).
    Combines research project and budget execution data.
    """
    STATUS_CHOICES = [
        ('집행완료', '집행완료'),
        ('처리중', '처리중'),
        ('취소', '취소'),
    ]

    execution_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique execution ID"
    )
    project_number = models.CharField(
        max_length=50,
        help_text="Project number"
    )
    project_name = models.CharField(
        max_length=255,
        help_text="Project name"
    )
    principal_investigator = models.CharField(
        max_length=100,
        help_text="Principal investigator name"
    )
    department = models.CharField(
        max_length=100,
        help_text="Department name"
    )
    funding_agency = models.CharField(
        max_length=255,
        help_text="Funding agency"
    )
    total_budget = models.BigIntegerField(
        help_text="Total budget (KRW)"
    )
    execution_date = models.DateField(
        help_text="Execution date"
    )
    execution_item = models.CharField(
        max_length=255,
        help_text="Execution item"
    )
    execution_amount = models.BigIntegerField(
        help_text="Execution amount (KRW)"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        help_text="Execution status"
    )
    note = models.TextField(
        null=True,
        blank=True,
        help_text="Additional notes"
    )

    class Meta:
        db_table = 'research_budget_data'
        indexes = [
            models.Index(fields=['project_number']),
            models.Index(fields=['department']),
            models.Index(fields=['execution_date']),
        ]
        ordering = ['-execution_date']

    def __str__(self):
        return f"{self.project_name} - {self.execution_item} ({self.execution_date})"


class UploadHistory(models.Model):
    """
    File upload history data model.
    Tracks all file upload activities.
    """
    FILE_TYPE_CHOICES = [
        ('department_kpi', 'Department KPI'),
        ('publication_list', 'Publication List'),
        ('research_project_data', 'Research Project Data'),
        ('student_roster', 'Student Roster'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User who uploaded the file"
    )
    file_name = models.CharField(
        max_length=255,
        help_text="Original file name"
    )
    file_type = models.CharField(
        max_length=50,
        choices=FILE_TYPE_CHOICES,
        help_text="Type of data file"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        help_text="Upload processing status"
    )
    records_processed = models.IntegerField(
        default=0,
        help_text="Number of records processed"
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        help_text="Error message if upload failed"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Upload timestamp"
    )

    class Meta:
        db_table = 'upload_history'
        indexes = [
            models.Index(fields=['-uploaded_at']),
        ]
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name} - {self.get_status_display()} ({self.uploaded_at})"
