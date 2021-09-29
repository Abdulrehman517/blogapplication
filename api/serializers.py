import pandas as pd
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'body', 'publish', 'status']


class UploadCsvSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, attrs):
        file = attrs.get('file')
        df = pd.read_csv(file)

        for index, row in df.iterrows():
            data_dict = {'title': row['Title'], 'slug': row['Title'], 'author': row['author'], 'Body': row['Body'],
                         'Publish': row['Publish'], 'Status': row['Status']}

            Post.objects.create(title=data_dict["title"], slug=data_dict["slug"], body=data_dict["Body"],
                            author_id=data_dict["author"], publish=data_dict['Publish'], status=data_dict['Status'])

        return attrs





