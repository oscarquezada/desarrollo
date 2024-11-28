from django.http import HttpResponseRedirect

class Custom404Middleware:
    """Middleware para redirigir errores 404 a la raíz de la API."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Si el error es 404, redirige a localhost:8000/api/
        if response.status_code == 404:
            # Redirige a la URL principal de la API
            return HttpResponseRedirect('/api/')
        return response
