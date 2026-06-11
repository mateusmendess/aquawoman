import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Aguardando banco de dados...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
            except OperationalError:
                self.stdout.write('Banco indisponível, aguardando 1s...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Banco disponível!'))
