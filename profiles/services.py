import requests
from rest_framework import status
from rest_framework.exceptions import APIException

GENDERIZE_URL = "https://api.genderize.io"
AGIFY_URL = "https://api.agify.io"
NATIONALIZE_URL = "https://api.nationalize.io"

class ExternalAPIException(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY

def fetch_gender(name):
    try:
        resp = requests.get(GENDERIZE_URL, params={'name': name}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        raise ExternalAPIException(detail="Genderize returned an invalid response")
    if data.get('gender') is None or data.get('count', 0) == 0:
        raise ExternalAPIException(detail="Genderize returned an invalid response")
    return {
        'gender': data['gender'],
        'gender_probability': data['probability'],
        'sample_size': data['count']
    }

def fetch_age(name):
    try:
        resp = requests.get(AGIFY_URL, params={'name': name}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        raise ExternalAPIException(detail="Agify returned an invalid response")
    if data.get('age') is None:
        raise ExternalAPIException(detail="Agify returned an invalid response")
    age = data['age']
    if age <= 12:
        age_group = "child"
    elif age <= 19:
        age_group = "teenager"
    elif age <= 59:
        age_group = "adult"
    else:
        age_group = "senior"
    return {'age': age, 'age_group': age_group}

def fetch_nationality(name):
    try:
        resp = requests.get(NATIONALIZE_URL, params={'name': name}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        raise ExternalAPIException(detail="Nationalize returned an invalid response")
    country_list = data.get('country', [])
    if not country_list:
        raise ExternalAPIException(detail="Nationalize returned an invalid response")
    best = max(country_list, key=lambda x: x['probability'])
    return {
        'country_id': best['country_id'],
        'country_probability': best['probability']
    }

def get_name_data(name):
    gender_info = fetch_gender(name)
    age_info = fetch_age(name)
    country_info = fetch_nationality(name)
    return {**gender_info, **age_info, **country_info}