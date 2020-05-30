$(function () {
    /* Functions */

    /* 1 - Infinite function to show and hide */
    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
          $('.loading').show();
        },
        onAfterPageLoad: function ($items) {
          $('.loading').hide();
        }
    });

    // to load in end of page
    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0]
    });
    /* 1 - end */

    /* 2 - Form interaction in Ajax with modal window*/
    var loadForm = function () {
        var target = $(this);
        $.ajax({
            url: target.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-add").modal("show");
            },
            success: function (data) {
                $("#modal-add .modal-content").html(data.html_objects);
            }
        });

    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#dataTable tbody").html(data.html_objects_list);  // <-- Replace the table body
                    $("#modal-add").modal("hide");  // <-- Close the modal
                } else {
                    $("#modal-add .modal-content").html(data.html_objects);
                }
            }
        });
        return false;
    };

    // Create object
    $(".js-add-object").click(loadForm);
    $("#modal-add").on("submit", ".js-add-object-form", saveForm);

    // Update object
    $("#dataTable").on("click", ".js-update-object", loadForm);
    $("#modal-add").on("submit", ".js-update-object-form", saveForm);

    // Delete object
    $("#dataTable").on("click", ".js-delete-object", loadForm);
    $("#modal-add").on("submit", ".js-delete-object-form", saveForm);
    /* 2 - End */
});