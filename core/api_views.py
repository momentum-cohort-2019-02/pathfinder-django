from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from core.pathfinder import ElevationMap, PathFinder, MapImage
from io import BytesIO
import base64


class ElevationMapSerializer(serializers.Serializer):
    elevation_data = serializers.CharField()
    show_path = serializers.BooleanField()


class ElevationMapView(APIView):

    def post(self, request, format=None):
        serializer = ElevationMapSerializer(data=request.data)
        if serializer.is_valid():
            map_data = serializer.data['elevation_data'].strip().split("\n")
            map = ElevationMap(data=map_data)
            pathfinder = PathFinder(map)
            map_image = MapImage(map, pathfinder)
            map_image.pathfinder.find_optimal_path()

            output = BytesIO()
            map_image.draw_image()
            if serializer.data['show_path']:
                map_image.draw_path()
            map_image.canvas.save(output, format='PNG')

            image_data = output.getvalue()
            image_data_url = 'data:image/png;base64,' + base64.b64encode(
                image_data).decode("utf-8")

            return Response({"data_url": image_data_url})


# ata = elevation_file.read().decode('utf-8').strip().split("\n")
#             map = ElevationMap(data=data)
#             pathfinder = PathFinder(map)
#             map_image = MapImage(map, pathfinder)
#             map_image.pathfinder.find_optimal_path()
#             print(map_image.canvas)

#             output = BytesIO()
#             map_image.draw_image()
#             map_image.draw_path()
#             map_image.canvas.save(output, format='PNG')

#             image_data = output.getvalue()
#             image_data_url = 'data:image/png;base64,' + base64.b64encode(
#                 image_data).decode("utf-8")
