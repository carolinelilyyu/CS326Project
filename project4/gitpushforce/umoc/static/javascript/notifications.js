/* Javascript Notification functionality. Makes AJAX request to /notifications/ and adds html to notifications dropdown. Allows dismissal of individual notifications, facilitated by AJAX. */

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

$(document).ready(function(){
	// make request to load notifications from server
	$.ajax({
		type: "get",
		url: "http://localhost:8000/notifications",
		contentType: "application/json",
		success: function(data) {
			// console.log('Received response');
			// console.log(data);
			
			// add rendered html to dropdown
			$('#notifications-dropdown').append(data);
			
			// set number of notifications 
			var num_notifications = $('.notification-li').length;
			$('#notifications-counter').text(num_notifications);
			
			// click handlers for each dismiss-notification-btn
			$('.dismiss-notification-btn').on('click', function() {
				var id = $(this).attr('id').substring(21);
				console.log('clicked to dismiss ' + id);
				
				// submit AJAX post saying notification was dismissed
				$.ajax({
					type: "POST",
					url: "http://localhost:8000/notifications",
					data: {'dismissed_id': id},
					success: function(result) {
						console.log(result);
						console.log('Removing #notification-li-' + id);
						// remove notification html
						$('#notification-li-' + id).remove();
						
						// subtract one from number of notifications
						$('#notifications-counter').text(parseInt($('#notifications-counter').text()) - 1);
						
					},
					error: function(result) {
						console.log('Error with POST');
						console.log(result)
						alert("Couldn't connect to server. Are you sure you're connected to the internet?");
						//console.log(result.responseText);
					}
				})
			});
		},
		error: function() {
			console.log("AJAX error: couldn't load notifications");
		}
	});
});