from rest_framework import serializers

from submission.models import Submission

# Serializer for Submission Model


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('code', 'language', 'input', 'status', 'output', 'error', 'exctime', 'mem')
