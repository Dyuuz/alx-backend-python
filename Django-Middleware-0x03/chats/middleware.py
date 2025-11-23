from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Write to logs/requests.log
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Restrict access outside 6AM - 9PM window
        # Task says: deny if user accesses chat outside 9PM and 6PM (meaning only allowed 6AM–9PM)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is restricted during this time.")

        return self.get_response(request)