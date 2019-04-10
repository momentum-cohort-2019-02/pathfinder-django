from django.shortcuts import render
from core.forms import PathfinderForm
from core.pathfinder import ElevationMap, PathFinder, MapImage
from io import BytesIO
import base64
# Create your views here.


def index_view(request):
    form = PathfinderForm()
    image_data_url = None

    if request.method == "POST":
        form = PathfinderForm(request.POST, request.FILES)
        if form.is_valid():
            elevation_file = request.FILES['elevation_file']
            data = elevation_file.read().decode('utf-8').strip().split("\n")
            map = ElevationMap(data=data)
            pathfinder = PathFinder(map)
            map_image = MapImage(map, pathfinder)
            map_image.pathfinder.find_optimal_path()
            print(map_image.canvas)

            output = BytesIO()
            map_image.draw_image()
            map_image.draw_path()
            map_image.canvas.save(output, format='PNG')

            image_data = output.getvalue()
            image_data_url = 'data:image/png;base64,' + base64.b64encode(
                image_data).decode("utf-8")

    return render(request, "core/index.html", {
        "form": form,
        "image_url": image_data_url
    })
