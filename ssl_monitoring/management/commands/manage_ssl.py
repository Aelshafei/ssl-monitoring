from django.core.management.base import BaseCommand, CommandError
from ssl_monitoring.ssl_checks import check_all_urls


class Command(BaseCommand):

	def handle(self, *args, **options):
		check_all_urls()