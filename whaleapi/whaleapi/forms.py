from django import forms
from django.conf import settings
import requests

class DictionaryForm(forms.Form):
    word = forms.CharField(max_length=100)

    def search(self):
        result = {}
        endpoint = 'https://whalemarket.saleswhale.io/whales/1'
        headers = {'Authorization': 'Bearer' + settings.BEARER_TOKEN}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:  # SUCCESS
            result = response.json()
            result['success'] = True
        else:
            result['success'] = False
            if response.status_code == 404:  # NOT FOUND
                result['message'] = 'No entry found for item'
            else:
                result['message'] = 'The Oxford API is not available at the moment. Please try again later.'
        return result
