function run_waitMe(effect) {
    $('body').waitMe({
        effect: effect,
        text: 'Extracting',
        bg: 'rgba(255,255,255,0.7)',
        color: '#09b9d6',
    });
}

Dropzone.options.idDropzone = {
    maxFilesize: 10, // MB
    thumbnailMethod: "contain",
    maxFiles: 4,
    acceptedFiles: "image/*",
    uploadMultiple: true,
    addRemoveLinks: true,
    autoProcessQueue: false,

    error: function (file, message, xhr) {
        if (xhr == null) this.removeFile(file);
        $("#id_message").text(message);
        $("#id_limit").modal("show");
    },

    init: function () {
        var submit_button = document.querySelector("#id_extract_data");
        var dz = this;
        submit_button.addEventListener("click", function () {
            dz.processQueue();
            run_waitMe("bounce");
        });
        dz.on("addedfile", function (file) {
            $("#id_extract_data").show();
        });
        dz.on("removedfile", function (file) {
            if (dz.getQueuedFiles().length === 0) {
                $("#id_extract_data").hide();
            }
        });
    }
};
