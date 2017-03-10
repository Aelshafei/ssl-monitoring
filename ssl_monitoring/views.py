from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import ssl, socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime
import sys
from .models import Url, Service, Environment, UrlCheck, SSL_CERTIFICATE_CASES
from .ssl_checks import check_url



# Create your views here.
def index(request):
	url_no = Url.objects.all().count()
	valid_certificates = Url.objects.filter(url_current_status='VLD').count()
	warning_certificates = Url.objects.filter(url_current_status='WRN').count()
	expired_certificates = url_no - valid_certificates - warning_certificates
	return render_to_response('index.html', {'valid_certificates': valid_certificates, 'warning_certificates': warning_certificates, 'expired_certificates': expired_certificates})

def instant_check(request, url):
	results = []
	hostname = url
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
	try:
		s.connect((hostname, 443))
		cert = s.getpeercert(True)
		cert_der = x509.load_der_x509_certificate(cert, default_backend())
		# 2015-04-12 23:59:59
		print(cert_der.not_valid_after)
		expiry_date = datetime.strptime(str(cert_der.not_valid_after), '%Y-%m-%d %H:%M:%S')
		print(expiry_date)
		if cert_der.signature_hash_algorithm.name == 'sha1':
			results.append({'message': 'SHA-1 Certificate', 'icon': 'fa-times', 'color': '#E60000'})
		elif datetime.now() > expiry_date:
			results.append({'message': 'Certificate has been expired since ' + str( (datetime.now() - expiry_date).days  ) + ' days!', 'icon': 'fa-times', 'color': '#E60000'})
		else:
			results.append({'message': 'SSL Certificate is valid and will expire after '  + str( (expiry_date - datetime.now()).days  ) + ' days' , 'icon': 'fa-check', 'color': '#5cb85c'})

	except:
		print("Unexpected error:", sys.exc_info())
		results.append({'message': 'URL is not Reachable', 'icon': 'fa-times', 'color': '#E60000'})
	return render_to_response('instant_check.html', {'url': url, 'results': results})


def services_list(request):
	data = []
	urls = Url.objects.all().order_by('-url_service')
	services = Service.objects.all()
	services_data = []
	for service in services:
		service_data = {'service_name': service.service_name, 'service_urls': [], 'service_valid': 0, 'service_warning': 0, 'service_danger': 0}
		service_environments = Environment.objects.filter(environment_service = service )
		service_valid = 0
		service_warning = 0
		service_danger = 0
		service_urls = []
		for environment in service_environments:
			environment_urls = Url.objects.filter(url_environment = environment) 
			for url  in environment_urls:
				if  url.url_current_status == '':
					url_status = check_url(url)
					print(url_status)
					url_status = UrlCheck(url_reference=url, url_status=url_status[0]['status'])
					url_status.save()
					url.url_current_status = url_status.url_status
					url.save()
				else:
					url_status = url.url_current_status
				url_status_string = [ d[1]  for d in SSL_CERTIFICATE_CASES if d[0] == url.url_current_status ][0]
				url_last_update = UrlCheck.objects.filter(url_reference = url).latest('check_date_time').check_date_time
				if url.url_current_status == 'VLD':
					url_row_color = 'success'
					service_valid += 1
				elif url.url_current_status == 'WRN':
					url_row_color = 'warning'
					service_warning += 1
				else:
					url_row_color = 'danger'
					service_danger += 1
				url_data = {'url': url, 'url_status': url_status, 'url_reason': url_status_string, 'url_last_update': url_last_update, 'url_row_color': url_row_color}
				service_urls.append(url_data)

		service_data['service_urls'] = service_urls
		service_data['service_valid'] = service_valid
		service_data['service_warning'] = service_warning
		service_data['service_danger'] = service_danger
		services_data.append(service_data)
	print(services_data)
	return render_to_response('services_list.html', {'services_data': services_data})

def how_to(request):
	return render_to_response('how_to.html')


