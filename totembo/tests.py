from django.test import TestCase
import requests
def get_next_page(request):
    next_page = request.META.get('HTTP_REFERER', 'main')
    return next_page


def get_dollar_rate():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()

        return data['rates']['UZS']

    except Exception as e:
        print(f'{e}')
        return 12500


def change_sum_to_dollar(sum):
    dollar = get_dollar_rate()
    return int((float(sum) / dollar) * 100)