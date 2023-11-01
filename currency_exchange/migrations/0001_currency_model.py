from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'symbol',
                    models.CharField(
                        verbose_name="currency's yfinance compatible symbol",
                        help_text='Only insert values which correspond to symbols supported by yfinance',
                        max_length=8,
                        unique=True
                    )
                ),
            ],
        ),
    ]
