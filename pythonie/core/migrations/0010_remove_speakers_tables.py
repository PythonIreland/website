# Generated manually to remove speakers app tables

from django.db import migrations


def drop_speakers_tables(apps, schema_editor):
    """
    Drop all tables from the removed speakers app.

    This migration removes tables that were part of the speakers app which
    has been completely removed from the codebase. The tables are dropped
    in order to handle foreign key constraints properly.
    """
    # We can't use apps.get_model() here since the speakers app is removed
    # Instead, we use raw SQL to drop the tables

    # Determine if we're using PostgreSQL or SQLite
    is_postgres = schema_editor.connection.vendor == "postgresql"
    cascade = " CASCADE" if is_postgres else ""

    with schema_editor.connection.cursor() as cursor:
        # For SQLite, we need to disable foreign keys temporarily
        if not is_postgres:
            cursor.execute("PRAGMA foreign_keys = OFF")

        # Drop tables in reverse dependency order
        # First drop junction tables (M2M relationships)
        cursor.execute(f"DROP TABLE IF EXISTS speakers_session_speakers{cascade}")

        # Then drop tables with foreign keys
        cursor.execute(f"DROP TABLE IF EXISTS speakers_session{cascade}")
        cursor.execute(f"DROP TABLE IF EXISTS speakers_speaker{cascade}")

        # Drop remaining tables
        cursor.execute(f"DROP TABLE IF EXISTS speakers_room{cascade}")
        cursor.execute(f"DROP TABLE IF EXISTS speakers_talkspage{cascade}")
        cursor.execute(f"DROP TABLE IF EXISTS speakers_speakerspage{cascade}")

        # Re-enable foreign keys for SQLite
        if not is_postgres:
            cursor.execute("PRAGMA foreign_keys = ON")


def reverse_drop_speakers_tables(apps, schema_editor):
    """
    This migration is irreversible.

    If you need to rollback, restore from a database backup taken before
    running this migration.
    """
    raise RuntimeError(
        "This migration cannot be reversed. "
        "The speakers app and its data have been permanently removed. "
        "Restore from a backup if you need to recover."
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_auto_20160703_0857"),
    ]

    operations = [
        migrations.RunPython(
            drop_speakers_tables,
            reverse_drop_speakers_tables,
        ),
    ]
