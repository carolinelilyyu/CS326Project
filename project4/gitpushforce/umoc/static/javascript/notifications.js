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
			console.log('Received response');
			console.log(data);
			
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
					dataType: "application/json",
					url: "http://localhost:8000/notifications",
					data: {'dismissed': id},
					success: function(result) {
						console.log(result);
						// remove notification html
						$('#notification-li-' + id).remove();
						
					},
					error: function(result) {
						console.log('Error with POST');
						console.log(result)
					}
				})
			});
		},
		error: function() {
			alert('AJAX error');
		}
	});
});