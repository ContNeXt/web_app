 /** This JS controls the home page
 **
 * @requires: jquery
 */

$(document).ready(function () {

    // Autocompletion in the first input
    $("#input-q").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/api/autocomplete/nodesjson",
                dataType: "json",
                data: {
                    q: request.term
                },
                success: function (data) {
                    response(data);
                }
            });
        },
        minLength: 2
    });
});