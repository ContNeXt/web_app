 /** This JS controls the home page
 **
 * @requires: jquery
 */

$(document).ready(function () {

    // Autocompletion in the first input
    $("#input-q").autocomplete({
        source: function (request, response) {
            $.ajax({
                type: "POST",
                url: "http://localhost:5000/api/autocomplete",
                dataType: "json",
                data: {
                    resource: $('#input-context').find(":selected").val(),
                    q: request.term
                },
                success: function (data) {
                    //alert(data)
                    // console.log(data)
                    response(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(textStatus + " " + errorThrown);
                }
            });
        },
        minLength: 2
    });
});