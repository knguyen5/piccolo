import typing as t
from unittest import TestCase

from piccolo.columns.column_types import Varchar
from piccolo.apps.migrations.auto import (
    DiffableTable,
    SchemaDiffer,
)


class TestSchemaDiffer(TestCase):
    def test_add_table(self):
        """
        Test adding a new table.
        """
        pass

    def test_drop_table(self):
        """
        Test dropping an existing table.
        """
        pass

    def test_rename_table(self):
        """
        Test renaming a table.
        """
        name_column = Varchar()
        name_column._meta.name = "name"

        schema: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Act", tablename="act", columns=[name_column]
            )
        ]
        schema_snapshot: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Band", tablename="band", columns=[name_column]
            )
        ]

        schema_differ = SchemaDiffer(
            schema=schema, schema_snapshot=schema_snapshot, auto_input="y"
        )

        self.assertTrue(len(schema_differ.rename_tables) == 1)
        self.assertEqual(
            schema_differ.rename_tables[0],
            "manager.rename_table(old_class_name='Band', new_class_name='Act', new_tablename='act')",  # noqa
        )

        self.assertEqual(schema_differ.create_tables, [])
        self.assertEqual(schema_differ.drop_tables, [])

    def test_add_column(self):
        """
        Test adding a column to an existing table.
        """
        name_column = Varchar()
        name_column._meta.name = "name"

        genre_column = Varchar()
        genre_column._meta.name = "genre"

        schema: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Band",
                tablename="band",
                columns=[name_column, genre_column],
            )
        ]
        schema_snapshot: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Band", tablename="band", columns=[name_column],
            )
        ]

        schema_differ = SchemaDiffer(
            schema=schema, schema_snapshot=schema_snapshot, auto_input="y"
        )

        self.assertTrue(len(schema_differ.add_columns) == 1)
        self.assertEqual(
            schema_differ.add_columns[0],
            "manager.add_column(table_class_name='Band', tablename='band', column_name='genre', column_class_name='Varchar', params={'length': 255, 'default': '', 'null': False, 'primary': False, 'key': False, 'unique': False, 'index': False})",  # noqa
        )

    def test_drop_column(self):
        """
        Test dropping a column from an existing table.
        """
        name_column = Varchar()
        name_column._meta.name = "name"

        genre_column = Varchar()
        genre_column._meta.name = "genre"

        schema: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Band", tablename="band", columns=[name_column],
            )
        ]
        schema_snapshot: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Band",
                tablename="band",
                columns=[name_column, genre_column],
            )
        ]

        schema_differ = SchemaDiffer(
            schema=schema, schema_snapshot=schema_snapshot, auto_input="y"
        )

        self.assertTrue(len(schema_differ.drop_columns) == 1)
        self.assertEqual(
            schema_differ.drop_columns[0],
            "manager.drop_column(table_class_name='Band', tablename='band', column_name='genre')",  # noqa
        )

    def test_rename_column(self):
        """
        Test renaming a column in an existing table.
        """
        name_column = Varchar()
        name_column._meta.name = "name"

        title_column = Varchar()
        title_column._meta.name = "title"

        schema: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Band", tablename="band", columns=[name_column],
            )
        ]
        schema_snapshot: t.List[DiffableTable] = [
            DiffableTable(
                class_name="Band", tablename="band", columns=[title_column],
            )
        ]

        schema_differ = SchemaDiffer(
            schema=schema, schema_snapshot=schema_snapshot, auto_input="y"
        )

        self.assertTrue(len(schema_differ.rename_columns) == 1)
        self.assertEqual(
            schema_differ.rename_columns[0],
            "manager.rename_column(table_class_name='Band', tablename='band', old_column_name='title', new_column_name='name')",  # noqa
        )
