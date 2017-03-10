import ssl, socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .models import Url, Service, Environment, UrlCheck
from datetime import datetime
import sys

def check_url(url):
	results = []
	#print(url.url_fqdn)
	hostname = url.url_fqdn
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
	try:
		s.connect((hostname, 443))
		cert = s.getpeercert(True)
		cert_der = x509.load_der_x509_certificate(cert, default_backend())
		# 2015-04-12 23:59:59
		#print(cert_der.not_valid_after)
		expiry_date = datetime.strptime(str(cert_der.not_valid_after), '%Y-%m-%d %H:%M:%S')
		#print(expiry_date)
		if cert_der.signature_hash_algorithm.name == 'sha1':
			results.append({'status': 'SHA1'})
		elif datetime.now() > expiry_date:
			results.append({'status': 'EXP',  'days': (datetime.now() - expiry_date).days })
		elif (expiry_date - datetime.now()).days < url.url_environment.environment_service.service_warning_setting :
			results.append({'status': 'WRN'})
		else:
			results.append({'status': 'VLD' , 'days': (expiry_date - datetime.now()).days })

	except:
		print("Unexpected error:", sys.exc_info())
		results.append({'status': 'NR'})
	return results

def check_all_urls():
	for url in Url.objects.all():
		url_status = check_url(url)
		url_status = UrlCheck(url_reference=url, url_status=url_status[0]['status'])
		url_status.save()
		url.url_current_status = url_status.url_status
		url.save()
	return None
