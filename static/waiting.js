// TODO: Add loading loop http://www.ajaxload.info/
// TODO: Add autocomplete form functionality https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform

$(document).ready(function () {

    $("#fakeloader").fakeLoader({
        timeToHide:1500, //Time in milliseconds for fakeLoader disappear
        zIndex:"999",//Default zIndex
        spinner:"spinner2",//Options: 'spinner1', 'spinner2', 'spinner3', 'spinner4', 'spinner5', 'spinner6', 'spinner7'
        bgColor:"#BB474B", //Hex, RGB or RGBA colors
        // imagePath:"yourPath/customizedImage.gif" //If you want can you insert your custom image
        });

    $.get('/get_image_url.json', function (image_url) {
        $('.yelp-image').attr('src', image_url);
        });

        var opts = {
                      lines: 7 // The number of lines to draw
                    , length: 34 // The length of each line
                    , width: 21 // The line thickness
                    , radius: 35 // The radius of the inner circle
                    , scale: 0.75 // Scales overall size of the spinner
                    , corners: 1 // Corner roundness (0..1)
                    , color: '#000' // #rgb or #rrggbb or array of colors
                    , opacity: 0.2 // Opacity of the lines
                    , rotate: 19 // The rotation offset
                    , direction: 1 // 1: clockwise, -1: counterclockwise
                    , speed: 0.9 // Rounds per second
                    , trail: 59 // Afterglow percentage
                    , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
                    , zIndex: 2e9 // The z-index (defaults to 2000000000)
                    , className: 'spinner' // The CSS class to assign to the spinner
                    , top: '50%' // Top position relative to parent
                    , left: '50%' // Left position relative to parent
                    , shadow: false // Whether to render a shadow
                    , hwaccel: false // Whether to use hardware acceleration
                    , position: 'absolute' // Element positioning
        }

        var target = document.getElementById('waiting');
        var spinner = new Spinner(opts).spin(target);

        $('.yelp-image').magnificPopup({
            type: 'image',
            closeOnContentClick: true,
            closeBtnInside: false,
            fixedContentPos: true,
            mainClass: 'mfp-no-margins mfp-with-zoom',
            image: {
                verticalFit: true
            },
            zoom: {
                enabled: false
            }
        });


        // var timer;
        // function poll () {
        //     return $.get('/status').then(function (data) {
        //         $('.poller__data').text(data.count);
        //         if (data.count < 100) {
        //             timer = setTimeout(poll, 500);
        //         }
        //     });
        // }

        // $('.poller__startButton').click(function (evt) {
        //     clearTimeout(timer);
        //     poll();
        // });


});