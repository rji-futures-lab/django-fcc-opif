from django.apps import apps
from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **options):

        self.model_name = options['model_name']
        storage = get_storage_class()()  

        try:
            self.model = apps.get_model('fcc_opif', self.model_name)
            if hasattr(self.model.objects, 'to_csv'):
                file_path = f'csv/{self.model.__name__}.csv'
                with storage.open(file_path, mode='wb') as f:
                    self.model.objects.to_csv(f)
        
        except LookupError:
            error_msg = f"{self.model_name} is not a defined model."
            self.stdout.write(
                self.style.ERROR(error_msg)
            )
            