from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import ssl, socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime
import sys



# Create your views here.
def index(request):
    return render_to_response('index.html')

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
			results.append({'message': 'SSL Certificate is valid and will expire after : '  + str( (expiry_date - datetime.now()).days  ) + ' days' , 'icon': 'fa-check', 'color': '#5cb85c'})

	except:
		print("Unexpected error:", sys.exc_info())
		results.append({'message': 'URL is not Reachable', 'icon': 'fa-times', 'color': '#E60000'})
	return render_to_response('instant_check.html', {'url': url, 'results': results})


