// TODO: Add loading loop http://www.ajaxload.info/
// TODO: Add autocomplete form functionality https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform

$(document).ready(function () {

    // initialize the 'starting-point' dropdown for future use
    var initialDropdownState = $('#venue-options').html();

    function getOptions(evt) {
        // set venueType to be the data value of the button clicked - 'bar' or 'restaurant'
        var venueType = $(this).data('venue-type');
        // make AJAX request using venueType to retrieve list of bar or restaurant options
        // create anonymous function as success handler to loop over returned JSON object
        // add options from object to dropdown
        $.get('/get_options.json', {'venue-type': venueType}, function (results) {
            // for each user click, first set the dropdown to initialDropdownState
            // so we don't append bar/restaurant options for multiple clicks
            $('#venue-options').html(initialDropdownState);
            // loop over the results and create a new <option> tag for each result
            for (var key in results) {
                var option = $('<option>');
                // set the value of the tag to the val we will use for the API calls
                option.attr('value', results[key]);
                // append the human-readable key to the variable option
                option.append(key);
                // append the variable option to venue-options
                $('#venue-options').append(option);
            }
        });
    }

// initialize the 'starting-point' list for future use
    var initialVisitState = $('#history-list').html();

    function getHistory(evt) {
        // set list to initial 'blank slate' list to avoid duplicates
        $('#history-list').html(initialVisitState);
        // make AJAX request to retrieve user visit history
        // create success handler to loop over returned JSON object
        // add visits to list using html string
        $.get('/get_history.json', function (visits) {
            for (var visit in visits) {
                var userVisit = '<li>' + visits[visit] + '</li>'
                $('#history-list').append(userVisit);
            }
        });
    }

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

    var target = document.getElementById('waiting')
    var spinner = new Spinner(opts).spin(target);

    $('.venue-option-btn').click(getOptions);
    $('#history-button').click(getHistory);

    var timer;
    function poll () {
        return $.get('/status').then(function (data) {
            $('.poller__data').text(data.count);
            if (data.count < 100) {
                timer = setTimeout(poll, 500);
            }
        });
    }

    $('.poller__startButton').click(function (evt) {
        clearTimeout(timer);
        poll();
    });

});