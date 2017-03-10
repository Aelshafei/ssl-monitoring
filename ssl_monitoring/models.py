from django.db import models

# Create your models here.
class Domain(models.Model):
	domain_name = models.CharField(max_length=50)
	domain_lead = models.EmailField(max_length=100)

	def __str__(self):
		return self.domain_name

class Service(models.Model):
	service_domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
	service_name = models.CharField(max_length=50)
	service_owner = models.EmailField(max_length=100)
	service_warning_setting = models.IntegerField(default=80)
	service_alert_setting = models.IntegerField(default=30)

	def __str__(self):
		return self.service_name

class Contact(models.Model):
	contact_email = models.EmailField(max_length=100)
	contact_services = models.ManyToManyField(Service)

	def __str__(self):
		return self.service_name

class Environment(models.Model):
	environment_service = models.ForeignKey(Service, on_delete=models.CASCADE)
	environment_name = models.CharField(max_length=50)
	is_environment_life = models.BooleanField()
	environment_server_user = models.CharField(max_length=30,default='weloadm')
	environment_server_hostname = models.CharField(max_length=50,default='localhost')

	def __str__(self):
		return str(self.environment_service) + '_' + str(self.environment_name)


SSL_CERTIFICATE_CASES = (
	('SHA1', 'Certificate is SHA-1'),
	('EXP', 'Certificate is Expired'),
	('NR', 'URL is not Reachable'),
	('VLD', 'Certificate is Valid'),
	('WRN', 'Certificate is about to expire')
	)

class Url(models.Model):
	url_environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
	url_fqdn = models.CharField(max_length=200)
	url_current_status = models.CharField(max_length=5, choices=SSL_CERTIFICATE_CASES, blank=True)
	#url_last_update = models.DateTimeField(blank=True)

	def __str__(self):
		return  str(self.url_fqdn) + ' @ ' + str(self.url_environment)


class UrlCheck(models.Model):
	url_reference = models.ForeignKey(Url, on_delete=models.CASCADE)
	url_status = models.CharField(max_length=5, choices=SSL_CERTIFICATE_CASES)
	check_date_time = models.DateTimeField(auto_now=True)


