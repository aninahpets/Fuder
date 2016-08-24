$(document).ready(function () {

function getBarOptions(evt) {
    $.get('/get_options.json', putBarOptions);
}

function putBarOptions(results) {
        $.each(results, function(val, text) {
            $'.venue-options'.append(
                $('<option></option>').val(val).html(text);
            );
        });
}

function alertMe(evt) {
    alert('Test');
}

$('#bar-button').click(alertMe);
// $('#restaurant-button').click(provideOptions);

});