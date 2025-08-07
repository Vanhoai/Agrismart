from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitingMiddleware(BaseHTTPMiddleware):
    # Rate limiting configurations
    RATE_LIMIT_DURATION = timedelta(minutes=1)
    RATE_LIMIT_REQUESTS = 100  # Maximum requests allowed in the duration

    def __init__(self, app):
        super().__init__(app)
        # Dictionary to store request counts for each IP
        self.request_counts = {}

    async def dispatch(self, request: Request, call_next):
        # Get the client's IP address
        client_ip = request.client.host  # type: ignore

        # Check if IP is already present in request_counts
        request_count, last_request = self.request_counts.get(client_ip, (0, datetime.min))

        # Calculate the time elapsed since the last request
        elapsed_time = datetime.now() - last_request

        if elapsed_time > self.RATE_LIMIT_DURATION:
            # If the elapsed time is greater than the rate limit duration, reset the count
            request_count = 1
        else:
            if request_count >= self.RATE_LIMIT_REQUESTS:
                # If the request count exceeds the rate limit, return a JSON response with an error message
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "statusCode": status.HTTP_429_TOO_MANY_REQUESTS,
                        "message": "Rate limit exceeded. Please try again later.",
                    },
                )

            request_count += 1

        # Update the request count and last request timestamp for the IP
        self.request_counts[client_ip] = (request_count, datetime.now())

        # Proceed with the request
        response = await call_next(request)
        return response
