function run_waitMe(effect) {
    $('body').waitMe({
        effect: effect,
        bg: 'rgba(255,255,255,0.7)',
        color: '#09b9d6',
    });
}

// Used for creating a new FileList object (input files which is used in django views is type of FileList).
function FileListItem(a) {
    a = [].slice.call(Array.isArray(a) ? a : arguments);
    for (var c, b = c = a.length, d = !0; b-- && d;) d = a[b] instanceof File
    if (!d) throw new TypeError("expected argument to FileList is File or array of File objects")
    for (b = (new ClipboardEvent("")).clipboardData || new DataTransfer; c--;) b.items.add(a[c])
    return b.files
}

Dropzone.options.idDropzone = {
    maxFilesize: 10, // MB
    thumbnailMethod: "contain",
    maxFiles: 4,
    acceptedFiles: "image/*",
    uploadMultiple: true,
    addRemoveLinks: true,
    autoProcessQueue: false,
    autoDiscover: false,

    error: function (file, message, xhr) {
        if (xhr == null) this.removeFile(file);
        $("#id_message").text(message);
        $("#id_limit").modal("show");
    },

    init: function () {
        var submit_button = document.querySelector("#id_extract_data");
        var dz = this;
        submit_button.addEventListener("click", function () {
            document.getElementById('id_hidden').files = FileListItem(dz.getQueuedFiles());
            run_waitMe("bounce");
            $("#id_submit_form").click();
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
