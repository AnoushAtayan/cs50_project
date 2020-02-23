$(document).ready(function() {
    "use strict";

    Dropzone.autoDiscover = false;
    Dropzone.options.id_dropzone = {
        paramName: "file", // The name that will be used to transfer the file
        maxFilesize: 2, // MB
        maxFiles: 4,
        thumbnailWidth: 300,
        thumbnailHeight: 400,
        acceptedFiles: "image/jpeg,image/png,image/gif",
        uploadMultiple: true,
        addRemoveLinks: true,
    };
});