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
// currently selected user object
var selected_user = null;
// currently selected admin level
var selected_level = null;

// mapping of admin level ids to words
var admin_mapping = {'a': 'Admin', 'l': 'Leader', 'u': 'User'};


// let user filter shown users by entering text in <user-filter>
$('#user-filter').bind('input', function() {
    // retrieve filter val, case-insensitive
	var filter = $(this).val().toLowerCase();

	// show items whose name contain a substring of filter text
    $('.user-select').each(function() {
		if ($(this).val().toLowerCase().includes(filter)) {
			$(this).show();
		} else {
			$(this).hide();
		}
	});
});

// handle user clicking an item in the <select> element, selecting a user
$('.user-select').on('click', function() {
	// id='user-select-<id>'
	var user_id = parseInt($(this).attr('id').substring(12));

	console.log('Clicked user ' + user_id);
	
	// populate UI with user data, if already in cache
	if (user_cache.has(user_id)) {
		populateUI(user_cache.get(user_id));
	}
	// make AJAX call to get user data if not already in cache
	else {
		$.ajax({
			type: 'GET',
			url: 'http://localhost:8000/administration_edit/',
			data: {'user_id': user_id },
			success: function(result) {
				// parse user data and add to cache
				user_cache.set(user_id, result)
				console.log('User cache now has ' + user_cache.get(user_id));
				
				populateUI(result);
			},
			error: function(result) { 
				console.log('Received error response:');
				console.log(result);
				console.log('Parsed ' + JSON.parse(result.responseText))
				alert("Couldn't connect to the server. Are you sure you have internet access?");
			}
		});
	}
});

// populates UI with data from given user
function populateUI(user) {
	// set selected_user 
	selected_user = user;
	
	if (selected_user === null) 
		return;
	if (selected_level !== null)
		$('#submit-btn').prop('disabled', false);
	
	console.log('Populating with obj ');
	console.log(user);
	
	$('#user-firstname').text(selected_user.first_name);
	$('#user-lastname').text(selected_user.last_name);
	$('#user-profile').html('<a href="' + selected_user.href + '">Click Here</a>');
	$('#user-email').text(selected_user.email);
	$('#user-adminlevel').text(admin_mapping[selected_user.admin_level]);
	
	/*$('#admin-level-box option[id="u"]').removeAttribute('selected');
	$('#admin-level-box option[id="l"]').removeAttribute('selected');
	$('#admin-level-box option[id="a"]').removeAttribute('selected');
	
	// set correct admin level selection
	//$('#admin-level-box').value = (selected_user.admin_level);
	$("#admin-level-box option[id='" + selected_user.admin_level + "']").attr("selected", "selected");*/
}

// handle user clicking Save button--check set admin level, and make POST request
$('#submit-btn').on('click', function() {
	console.log('User wants to submit');
	console.log(selected_user);
	
	if (selected_user === null) 
		return;
	
	// retrieve level selected in admin-level-box
	var selected_level = $("#admin-level-box option:selected").attr("id");
	
	// check selected admin level is different from original before making POST
	if (selected_level != selected_user.admin_level) {
		console.log('Detected change');
		
		$.ajax({
			type: 'POST',
			dataType: 'application/json',
			url: 'http://localhost:8000/administration_edit/',
			data: {'user_id': selected_user.id, 'admin_level': selected_level},
			success: function(result) {
				console.log('Received successful response ' + result)
				// TODO: SET SELECTED TO PROPER ADMIN LEVEL
			},
			error: function(result) { // TODO: WHY IS THIS ALWAYS AN ERROR?
				console.log('Received error response ' + result.responseText)
				
				// update admin level on selected user
				selected_user.admin_level = selected_level;
			}
		});
	}
});

// enable submit button (since user and admin level have been selected)
$('#admin-level-box').on('change', function() {
	selected_level = $(this).val;
	console.log(selected_level);
	if (selected_user !== null)
		$('#submit-btn').prop('disabled', false);
});