from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0003_remove_studentenrollment_batch_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentenrollment",
            name="batch",
            field=models.ForeignKey(
                to="academics.batch",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enrollments",
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="studentenrollment",
            name="end_date",
            field=models.DateField(null=True, blank=True),
        ),
    ]
