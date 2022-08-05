from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import Response, APIView
from rest_framework import status

from .serializers import ProcessPhotoInputSerializer
from .processors import RemoveBackground

class ProcessPhoto(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProcessPhotoInputSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(serializer.validated_data)

    def on_valid_request_data(self, data):
        photo = data['photo']
        width = data['width']
        height = ['height']
        background = ['background']
        enhance = ['enhance']

        print(photo)
        result = RemoveBackground(photo)

        return Response({
            'code': status.HTTP_200_OK,
            'message': _('Operation successful'),
        }, status=status.HTTP_201_CREATED)

