from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from counterservice.models import URLs
from counterservice.serializers import URLsSerializer
import validators
import django_rq
from counterservice.parser import parse


class CounterService(APIView):
    def get(self, request, pk):
        try:
            url = URLs.objects.get(pk=pk)
            return Response({'result': url.result}, 200)
        except URLs.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Validate that URL is present in requset
        if 'url' not in request.data:
            return Response({'error': 'URL is not present'}, 400)
        # Validate that URL is a valid URL
        elif not validators.url(request.data['url']):
            return Response({'error': 'Given URL is invalid'}, 400)
        # Validate that URL is a HTTP or HTTPS resource
        elif not (request.data['url'].startswith('http://') or request.data['url'].startswith('https://')):
            return Response({'error': 'URL must be an http or htts resource'}, 400)

        serializer = URLsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            django_rq.enqueue(parse, serializer.data['id'])

            return Response({'id': serializer.data['id']}, 201)

        return Response({'error': 'Error while saving URL'}, 400)
