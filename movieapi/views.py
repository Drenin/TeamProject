import json
import urllib.request
from pprint import pprint
from django.shortcuts import render


def index(request):
    return render(request, 'movieapi/index.html')

def search(request):
    if request.method == 'GET':

        client_id = "받아온 API ID"
        client_secret = "받아온 API PW"

        q = request.GET.get('q')
        encText = urllib.parse.quote("{}".format(q))
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText  # json 결과
        movie_api_request = urllib.request.Request(url)
        movie_api_request.add_header("X-Naver-Client-Id", client_id)
        movie_api_request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(movie_api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            pprint(result)

            context = {
                'items': items
            }
            return render(request, 'movieapi/search.html', context=context)
