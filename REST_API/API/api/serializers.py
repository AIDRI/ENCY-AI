from rest_framework import serializers
import sys
from API.models import TextSummarizer
sys.path.append('..')
from AI.test import prediction
from AI.models.word_extraction import word_extraction



class TextSummarizerSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True, max_length=100000)
    length = serializers.IntegerField(required=True, min_value=2)
    output = serializers.CharField(read_only=True)
    keywords = serializers.CharField(read_only=True)

    class Meta:
        model = TextSummarizer
        fields = ('text', 'length', 'output', "keywords")

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        output1 = prediction(validated_data['text'], validated_data['length'])

        output = ""
        for i in output1:
            output += i

        try:
            key_words = word_extraction(output)
        except:
            key_words = "The keyword extractor doesn't found keywords to output. Try to verify if the sentence is correct, or if the construction is ok !"


        return {
            'output': output,
            'keywords': key_words,
            'text': validated_data['text'],
            'length': validated_data['length'],
        }
