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
from .processors import remove_background, detect_face, prepare_printable_4R
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

        # Save image in DB
        object = photo_model.create_photo(photo=photo, title=photo, width=width, height=height)

        # Step 1: Read image
        image = cv2.imread(settings.MEDIA_ROOT + str(object.photo))

        if image is None:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': _('A problem related to image happened'),
            }, status=status.HTTP_400_BAD_REQUEST)

        # Step2: Crop image
        cropped = detect_face(image, 600, 600, 310)

        if cropped is None:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': _('No face detected in the image'),
            }, status=status.HTTP_400_BAD_REQUEST)

        # Step3: Remove background
        result = remove_background(cropped)

        trans_mask = result[:, :, 3] == 0
        result[trans_mask] = [255, 255, 255, 255]
        single = cv2.cvtColor(result, cv2.COLOR_BGRA2BGR)

        single_file_path = settings.OUTPUT_ROOT + str(object.uuid) + "-single.png"
        cv2.imwrite(single_file_path, single)

        single_file_url = "http://" + request.get_host() + settings.MEDIA_URL + settings.OUTPUT_PHOTO_URL + str(
            object.uuid) + "-single.png"
        object.single = single_file_url


        # Step 4: Prepare printable multi image
        multi = prepare_printable_4R(single)

        multi_file_path = settings.OUTPUT_ROOT + str(object.uuid) + "-multi.png"
        cv2.imwrite(multi_file_path, multi)

        multi_file_url = "http://" + request.get_host() + settings.MEDIA_URL + settings.OUTPUT_PHOTO_URL + str(
            object.uuid) + "-multi.png"
        object.multi = multi_file_url

        object.save()

        serialized_data = PhotoModelSerializer(object, many=False, context={"request": request}).data

        return Response({
            'code': status.HTTP_200_OK,
            'message': _('Operation successful'),
            'photo': serialized_data
        }, status=status.HTTP_200_OK)
