from django.shortcuts import render

from .forms import ImageForm
from .utils import handle_image_file


def faces_extractor(request):
    form = ImageForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            extracted_img_list, nickname_list = handle_image_file(image=request.FILES['image'])
            return render(request, "pages/image/image_output.html",
                          {'extracted_img_list': extracted_img_list,
                           'nickname_list': nickname_list})

    return render(request, "pages/image/image_input.html", {'form': form})
