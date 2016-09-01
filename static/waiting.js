// TODO: Add loading loop http://www.ajaxload.info/
// TODO: Add autocomplete form functionality https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform

$(document).ready(function () {

    $("#fakeloader").fakeLoader({
        timeToHide:1500,
        zIndex:"999",
        spinner:"spinner2",
        bgColor:"#EE6E73"
        });

    $.get('/get_image_url.json', function (image_url) {
        $('.yelp-image').attr('src', image_url);
        });
});