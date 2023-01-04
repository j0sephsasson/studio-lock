function populateModal(event) {
    var studio = document.getElementById('studio_name').value;
    var date = document.getElementById('date').value;
    var time_slot = document.getElementById('time_slot').value;
    var engineer = document.getElementById('engineer').value;

    if (studio === '' || date === '' || time_slot === '' || engineer === '') {
        // One or more options are null, so do not open the modal
        alert('Please Select All Options.')
        location.reload();
        return;
    }

    var time_object = {
        '1': '12PM-4PM',
        '2': '4PM-8PM',
        '3': '8PM-12AM'
    }

    var actual_time = time_object[time_slot]

    document.getElementById('studio_selection').innerHTML = studio;
    document.getElementById('date_selection').innerHTML = date;
    document.getElementById('time_selection').innerHTML = actual_time;
    document.getElementById('engineer_selection').innerHTML = engineer;

    document.getElementById('studio_selection').value = studio;
    document.getElementById('date_selection').value = date;
    document.getElementById('time_selection').value = actual_time;
    document.getElementById('engineer_selection').value = engineer;

    // console.log(studio, date, time_slot, engineer);
};

function completeBooking() {
    var studio = document.getElementById('studio_selection').value;
    var date = document.getElementById('date_selection').value;
    var time = document.getElementById('time_selection').value;
    var engineer = document.getElementById('engineer_selection').value;

    var time_object = {
        '12PM-4PM': '1',
        '4PM-8PM': '2',
        '8PM-12AM': '3'
    };

    var slot_time = time_object[time];

    $j.ajax({
        type: 'POST',
        url: '/booking_checker',
        data: {
            studio: studio,
            date: date,
            slot: slot_time,
            engineer: engineer
        },
        success: function (response) {
            console.log(response);
            document.getElementById('bookStudio').value = studio;
            document.getElementById('bookDate').value = date;
            document.getElementById('bookTime').value = slot_time;
            document.getElementById('bookEngineer').value = engineer;
            document.getElementById('booking-form').submit();
        },
        error: function(xhr, status, error) {
            console.log('Error: ' + error);
        }
    });
};