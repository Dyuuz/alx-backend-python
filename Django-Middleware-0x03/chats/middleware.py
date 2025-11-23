from datetime import datetime, timedelta
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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request times per IP: { "127.0.0.1": [timestamp1, timestamp2] }
        self.ip_tracking = {}

    def __call__(self, request):
        # Only limit POST messages (chat messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Create record for new IP
            if ip not in self.ip_tracking:
                self.ip_tracking[ip] = []

            # Remove timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.ip_tracking[ip] = [
                t for t in self.ip_tracking[ip] if t > one_minute_ago
            ]

            # Check limit (5 messages/min)
            if len(self.ip_tracking[ip]) >= 5:
                return HttpResponseForbidden(
                    "Message limit exceeded. Try again in a minute."
                )

            # Record this message timestamp
            self.ip_tracking[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Extract IP address from request safely.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
    

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Ensure user is authenticated
        if not user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this resource.")

        # Expecting a role field on the user model (e.g., user.role = "admin")
        # Allowed roles
        allowed_roles = ["admin", "moderator"]

        # If user role not allowed → block
        user_role = getattr(user, "role", None)

        if user_role not in allowed_roles:
            return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)