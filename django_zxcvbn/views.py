import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django_zxcvbn_field.services.validate_password_service import (
    ValidatePasswordService)


@csrf_exempt
def zxcvbn_validator_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        password = data.get('password')
        results = ValidatePasswordService(password).call()
        return JsonResponse(results)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
