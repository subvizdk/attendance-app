from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Course, Batch, Student, StudentEnrollment, TeacherAssignment
from .forms import StudentImportForm
from .importers import import_students_from_xlsx
from .admin_forms import BulkEnrollForm

admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(TeacherAssignment)


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "batch", "start_date", "end_date")
    list_filter = ("batch", "batch__branch")
    search_fields = ("student__full_name", "student__admission_no")

    def save_model(self, request, obj, form, change):
        # Friendly validation: only one active enrollment
        if obj.end_date is None:
            exists = StudentEnrollment.objects.filter(
                student=obj.student,
                end_date__isnull=True
            ).exclude(pk=obj.pk).exists()
            if exists:
                raise ValidationError("This student already has an active enrollment. End the previous enrollment first.")
        super().save_model(request, obj, form, change)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "admission_no",
        "branch",
        "father_full_name",
        "mother_full_name",
        "email",
        "phone",
    )
    search_fields = (
        "full_name",
        "admission_no",
        "father_full_name",
        "mother_full_name",
        "email",
    )
    list_filter = ("branch",)

    # Add import button on the student list
    change_list_template = "admin/academics/student_changelist.html"

    actions = ["bulk_enroll_action"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-excel/", self.admin_site.admin_view(self.import_excel), name="student-import-excel"),
            path("bulk-enroll/", self.admin_site.admin_view(self.bulk_enroll_view), name="student-bulk-enroll"),
        ]
        return custom_urls + urls

    # -------------------------
    # Excel Import
    # -------------------------
    def import_excel(self, request):
        if request.method == "POST":
            form = StudentImportForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data["file"]
                summary, errors = import_students_from_xlsx(file)

                messages.success(
                    request,
                    f"Import complete. Created: {summary['created']} | Updated: {summary['updated']} | Enrolled/Moved: {summary['enrolled']}"
                )

                if errors:
                    for err in errors[:15]:
                        messages.error(request, f"Row {err['row']}: {err['error']}")
                    if len(errors) > 15:
                        messages.error(request, f"...and {len(errors) - 15} more errors.")

                return redirect("..")
        else:
            form = StudentImportForm()

        context = {"form": form, "title": "Import Students from Excel (.xlsx)"}
        return render(request, "admin/academics/import_students.html", context)

    # -------------------------
    # Bulk Move selected students to a batch
    # -------------------------
    def bulk_enroll_action(self, request, queryset):
        selected = queryset.values_list("id", flat=True)
        return redirect(f"bulk-enroll/?ids={','.join(str(i) for i in selected)}")

    bulk_enroll_action.short_description = "Move selected students to a batch"

    @transaction.atomic
    def bulk_enroll_view(self, request):
        ids_param = request.GET.get("ids", "")
        student_ids = [s for s in ids_param.split(",") if s.strip().isdigit()]

        if not student_ids:
            messages.error(request, "No students selected.")
            return redirect("../")

        students = Student.objects.filter(id__in=student_ids)

        if request.method == "POST":
            form = BulkEnrollForm(request.POST)
            if form.is_valid():
                batch = form.cleaned_data["batch"]
                start_date = form.cleaned_data["start_date"] or now().date()

                # Safety: ensure all students are in same branch as batch
                bad_branch = students.exclude(branch=batch.branch)
                if bad_branch.exists():
                    messages.error(
                        request,
                        f"Some selected students are not in the same branch as the batch ({batch.branch.city_name}). "
                        f"Select a different batch or fix student branches."
                    )
                    return redirect(request.path + f"?ids={ids_param}")

                moved_count = 0

                for student in students:
                    # End current active enrollment (if any)
                    StudentEnrollment.objects.filter(
                        student=student,
                        end_date__isnull=True
                    ).update(end_date=now().date())

                    # Create new active enrollment
                    StudentEnrollment.objects.create(
                        student=student,
                        batch=batch,
                        start_date=start_date,
                        end_date=None,
                    )
                    moved_count += 1

                messages.success(request, f"Moved {moved_count} students into batch: {batch}")
                return redirect("../")

        else:
            form = BulkEnrollForm(initial={"_selected_action": student_ids})

        context = {
            "title": "Move Students to a Batch",
            "students": students.order_by("full_name"),
            "form": form,
            "ids_param": ids_param,
        }
        return render(request, "admin/academics/bulk_enroll_students.html", context)
