from .models import Visitor

class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the visitor's IP address
        ip_address = self.get_client_ip(request)

        # Create a Visitor object and save it to the database
        if ip_address:
            Visitor.objects.create(ip_address=ip_address)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
