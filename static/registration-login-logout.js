$(document).ready(function () {

function setUpForRide(evt) {
    evt.preventDefault();

    var formInputs = {'user-address': $('#field-user-address').val()};

    $.post('/get_user_auth',
            formInputs,
            confirmRide
            );
}

function confirmRide() {
    alert('Your Uber is on its way');
}

$('#request-ride-button').click(setUpForRide);

}
)
