from rest_framework import serializers
import sys
from API.models import TextSummarizer
sys.path.append('..')
from AI.test import prediction
from AI.wiki import search_on_wikipedia
from AI.models.word_extraction import word_extraction


choices = [
    ('yes', 'yes'),
    ('no', 'no')
]

class TextSummarizerSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True, max_length=100000)
    length = serializers.IntegerField(required=True, min_value=2)
    use_keywords = serializers.ChoiceField(choices=choices, required=True)
    output = serializers.CharField(read_only=True)
    keywords = serializers.CharField(read_only=True)
    websites = serializers.CharField(read_only=True)

    class Meta:
        model = TextSummarizer
        fields = ('text', 'length', 'use_keywords', 'output', "keywords", "websites")

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        output1 = prediction(validated_data['text'], validated_data['length'])
        output = ""
        for i in output1:
            output += i

        if validated_data['use_keywords'] == 'yes':
            try:
                key_words = word_extraction(output)
                websites = search_on_wikipedia(key_words)
            except:
                key_words = "The keyword extractor doesn't found keywords to output. Try to verify if the sentence is correct, or if the construction is ok !"
                websites = "As a result, the AI cannot find websites !"

            return {
                'output': output,
                'keywords': key_words,
                'websites': websites,
                'text': validated_data['text'],
                'length': validated_data['length'],
                'use_keywords': validated_data['use_keywords'],
            }
        else:
            return {
                'output': output,
                'text': validated_data['text'],
                'length': validated_data['length'],
                'use_keywords': validated_data['use_keywords'],
            }