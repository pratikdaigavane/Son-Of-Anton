import os
import json
import base64
import pika  # Pika client for RabbitMQ
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import logging

db_logger = logging.getLogger('customLog')

# Django Rest Framework dependencies
from rest_framework import generics
from rest_framework.response import Response

# Model and serializer dependencies
from submission.models import Submission
from submission.serializer import SubmissionSerializer


# Class-based view for Check API
class Check(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    def get_queryset(self):
        subid = self.kwargs['subid']
        return Submission.objects.filter(id=subid)


# Function-based view for Submit API
def Submit(request):
    try:
        if len(json.loads(request.body.decode())['code']) <= 0:
            return HttpResponse(status=400)  # Invalid Code
        sub = Submission(code=json.loads(request.body.decode())['code'],
                         input=json.loads(request.body.decode())['input'],
                         language=json.loads(request.body.decode())['language'])
        sub.save()  # Save the code, input and language to database.
    except:
        return HttpResponse(status=400)  # Invalid code, input or language
    try:
        # Add task to RabbitMQ
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.environ.get('RABBITMQ_HOST', 'localhost'), credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              properties=pika.BasicProperties(delivery_mode=2),
                              body=str(sub.id))
        return JsonResponse({'subid': sub.id})  # Successfully saved to DB and added to RabbitMQ
    except:
        return HttpResponse(status=500)  # Pika or RabbitMQ error


def doc(req):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    fs = open(os.path.join(__location__, "api.html"), 'r')
    data = fs.read()
    return HttpResponse(data)


def apispec(req):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    fs = open(os.path.join(__location__, "api.json"), 'r')
    data = fs.read()
    response = HttpResponse(data)
    response['content-disposition'] = 'attachment; filename="Mocha Compiler.json"'
    return response
