// Handles loading and replying to comments. Retrieves comments for given trip id using AJAX.

function getCookie(name) {
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
console.log('Got CSRF token: ' + csrftoken);

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
	// query trip comments and append HTML
	$.ajax({
		type: "get",
		url: "http://localhost:8000/trip/" + trip_id + "/comments",
		contentType: "application/json",
		success: function(data) {
			console.log('Received response');
			console.log(data);
			
			// append rendered comment section below comments-header element
			$('#comments-header').append(data);
			
			// create click handlers for each reply button
			$('.comment-reply-btn').on('click', function() {
				// extract comment id ("reply-btn-<id>")
				var id = $(this).attr('id').substring(10);
				console.log('clicked ' + id);
				
				// remove reply button from parent comment
				$(this).remove();
				
				// create input element for reply
				var reply_input = $('<input/>', {
					id: 'reply-input-' + id
				});
			
				// create button to submit reply
				var reply_btn = $('<button/>', {
					text: 'Reply', //set text 1 to 10
					id: 'submit-btn-' + id,
					click: function () { 
						console.log('Clicked submit on ' + id);
						// submit AJAX post with reply data
						$.ajax({
							type: "POST",
							dataType: "application/json",
							url: "http://localhost:8000/trip/" + trip_id + "/comments",
							data: {'text': reply_input.val(), 'parent': id},
							success: function(result) {
								console.log(result);
								
							},
							error: function(result) {
								console.log('Error with POST');
								console.log(result)
							}
						})
					}
				});
				
				// add input element and button after comment's div
				$('#comment-' + id).after(reply_input);
				$('#reply-input-' + id).after(reply_btn);
				
			});
		},
		error: function(){
			console.log('AJAX error');
		}
	});
});