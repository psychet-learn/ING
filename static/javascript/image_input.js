$(document).ready(function() {
    $('#id_image').on('change', function () {
        var file = this.files[0];
        var form_data = new FormData();
        form_data.append('file', file);

        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preview_input_image')
                .attr('src', e.target.result)
                .width(400);
        };
        reader.readAsDataURL(file);
    });
});
