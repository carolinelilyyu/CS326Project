/* Javascript site administration functionality. Supports filtering of <select> for users and populating user data. Manages AJAX calls to get user data and post changes. */

function getCookie(name) {  // TODO: IMPORT ON ALL SCRIPTS
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// cookie is 'csrftoken', HTTP header is 'X-CRSFToken'
var csrftoken = getCookie('csrftoken');

// TODO: MAKE SURE GETCOOKIE FUNCTION IMPLEMENTED
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// cache of user data. Mapped user_id->User object parsed from JSON
var user_cache = new Map()

// handle user clicking an item in the <select> element, selecting a user
$('.user-select').on('click', function() {
	// id='user-select-<id>'
	var user_id = $(this).attr('id').substring(12);

	console.log('Clicked user ' + user_id);
	// check if user data in cache
	
	// make AJAX query to get JSON data for queried user
	$.ajax({
		type: 'GET',
		dataType: 'application/json',
		url: 'http://localhost:8000/administration_edit',
		data: {'user_id': user_id },
		success: function(result) {
			console.log('Received successful response ' + result)
		},
		error: function(result) { // TODO: WHY IS THIS ALWAYS AN ERROR?
			console.log('Received error response ' + result)
			console.log(result)
			console.log(JSON.parse(result.responseText))
		}
	});
});