 /** This JS controls the home page
 **
 * @requires: jquery
 */

$(document).ready(function () {

    // Autocompletion in the first input
    $('#input_q').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/api/autocompletion/pathway_name",
                dataType: "json",
                data: {
                    resource: $('#select-1').find(":selected").val(),
                    q: request.term
                },
                success: function (data) {
                    response(data); // functionName
                }
            });
        }, minLength: 2
    });

});