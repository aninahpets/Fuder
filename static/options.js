$(document).ready(function () {

    function getOptions(evt) {
        // initialize the 'blank' dropdown
        var initialDropdownState = $('#venue-options').html();
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
            for (key in results) {
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

    $('.venue-option-btn').click(getOptions);

});