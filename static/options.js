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


    $('.venue-option-btn').click(getOptions);
    $('#history-button').click(getHistory);


});