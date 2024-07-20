import os
from main.models import Stats
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

# Create your views here.
PARSING_URL = os.getenv("URL", 'https://open-meteo.com/')


class StartWeatherView(APIView):
    template_name = 'some_shit.templates'

    def get(self, request):
        if request:
            city = self.request.data
            try:
                result = request.get(f'PARSING_URL/{city}')
                if result:
                    prepare(result)
                    check_new_or_add(result[name])
                    return Response(data=result, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                print(e)

        return Response(status=status.HTTP_400_BAD_REQUEST)


def request_stats(request):
    if request:
        query = Stats.objects.get(city=request.get.params)
        if query:
            return Response(data={query}, status=status.HTTP_200_OK, template_name='stat.templates')
        return Response(data={"This city had 0 requests"}, status=status.HTTP_204_NO_CONTENT, template_name='stat.templates')
