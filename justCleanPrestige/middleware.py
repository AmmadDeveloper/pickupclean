from django.shortcuts import redirect


class RequestCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("custom middleware before next middleware/view")
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        update_url=False

        url=request.build_absolute_uri()

        if url[0:5]!='https':
            url=f'https{url[4:]}'
            update_url=True
        if url[9:12]!='www':
            url=f'{url[0:8]}www.{url[8:]}'
            update_url=True

        if update_url:
            return redirect(url)
        response = self.get_response(request)

        # Code to be executed for each response after the view is called
        #
        print("custom middleware after response or previous middleware")

        return response