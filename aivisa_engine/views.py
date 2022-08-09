import io
import numpy as np
from PIL import Image
import cv2

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import Response, APIView
from rest_framework import status

from .serializers import ProcessPhotoInputSerializer, PhotoModelSerializer
from .processors import remove_background, detect_face
from .models import Photo as photo_model


class ProcessPhoto(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProcessPhotoInputSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(serializer.validated_data, request)

    def on_valid_request_data(self, data, request):
        photo = data.get('photo')
        width = data.get('width')
        height = data.get('height')
        red = data.get('red')
        green = data.get('green')
        blue = data.get('blue')
        enhance = data.get('enhance')

        image = Image.open(io.BytesIO(photo.read()))

        object = photo_model.create_photo(photo=photo, title=photo, width=width, height=height)

        image = cv2.imread(settings.MEDIA_ROOT + str(object.photo))

        if image is None:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': _('A problem related to image happened'),
            }, status=status.HTTP_400_BAD_REQUEST)

        cropped = detect_face(image, 600, 600, 310)
        result = remove_background(cropped)

        result_file_path = settings.OUTPUT_ROOT + str(object.uuid) + ".png"
        cv2.imwrite(result_file_path, result)

        result_file_url = "http://" + request.get_host() + settings.MEDIA_URL + settings.OUTPUT_PHOTO_URL + str(object.uuid) + ".png"
        object.result = result_file_url
        object.save()

        serialized_data = PhotoModelSerializer(object, many=False, context={"request": request}).data

        return Response({
            'code': status.HTTP_200_OK,
            'message': _('Operation successful'),
            'photo': serialized_data
        }, status=status.HTTP_200_OK)

