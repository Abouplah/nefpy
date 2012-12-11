# encoding: utf-8

from django import db
from django.db.models import signals

import auf.django.references.models


def post_syncdb(sender, **kwargs):
    """Création des vues vers datamaster."""

    verbosity = kwargs.get('verbosity', 1)

    # On ne crée des vues que si on est sur une BD MySQL.
    # L'attribut db.connection.vendor n'est présent qu'à partir de Django
    # 1.3
    if (hasattr(db.connection, 'vendor')
        and db.connection.vendor != 'mysql') or \
       'mysql' not in db.backend.__name__:
        return

    cursor = db.connection.cursor()

    # Vérifions qu'on a une BD qui s'appelle 'datamaster'
    if not cursor.execute("SHOW DATABASES LIKE 'datamaster'"):
        return

    # Déterminons la liste de tables de référence dans datamaster
    cursor.execute("SHOW TABLES IN datamaster LIKE 'ref\\_%%'")
    datamaster_tables = set(row[0] for row in cursor)

    # Déterminons la liste de tables que nous avons déjà et
    # enlevons-les des tables de datamaster
    cursor.execute("SHOW FULL TABLES WHERE Table_type != 'VIEW'")
    my_tables = set(row[0] for row in cursor)
    datamaster_tables.difference_update(my_tables)

    # On peut maintenant créer les vues
    if verbosity > 0:
        print u"Création des vues vers datamaster"
    cursor = db.connection.cursor()
    schema = db.connection.settings_dict['NAME']
    for table in datamaster_tables:
        if verbosity > 1:
            print u"Création d'une vue vers datamaster.%s" % table
        cursor.execute(
            'CREATE OR REPLACE VIEW `%s` AS SELECT * FROM datamaster.`%s`' %
            (table, table)
        )

        # Vérifions s'il y a des foreign keys vers cette vue.
        cursor.execute(
            '''
            SELECT TABLE_NAME, CONSTRAINT_NAME
            FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = %s AND REFERENCED_TABLE_NAME = %s
            ''',
            (schema, table)
        )
        for row in cursor:
            db.connection.cursor().execute(
                'ALTER TABLE %s DROP FOREIGN KEY %s' % row
            )


signals.post_syncdb.connect(post_syncdb, sender=auf.django.references.models)
