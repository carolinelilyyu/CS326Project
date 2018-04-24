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

// set up on-click for base reply button to create a new comment
$('#base-reply-btn').on('click', function() { 
	
	// disable base reply button 
	$('#base-reply-btn').prop('disabled', true);

	// create reply and add it beneath new comment button
	// $('#base-reply-btn').after(createReply(0));
	createReply(0, $('#base-reply-btn'));
});

$(document).ready(function(){
	// query trip comments and append HTML
	$.ajax({
		type: "get",
		url: "http://localhost:8000/trip/" + trip_id + "/comments",
		contentType: "application/json",
		success: function(data) {
			// append rendered comment section below base-reply-btn element
			$('#base-reply-btn').after(data);
			
			// create click handlers for each reply button
			$('.comment-reply-btn').on('click', function() {
				// extract comment id ("reply-btn-<id>")
				var id = $(this).attr('id').substring(10);
				console.log('clicked ' + id);
				
				
				// remove reply button from parent comment
				$(this).remove();
				
				// create reply and add it after comment's div
				//$('#comment-' + id).after(createReply(id));
				createReply(id, $('#comment-' + id));
				
				console.log($('#reply-' + id).html())
			});
		},
		error: function(){
			console.log('AJAX error');
		}
	});
});

// creates html object for a reply to the given comment. Can be added into the page. Adds it after the given root_elem var
function createReply(id, root_elem) {
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
				url: "http://localhost:8000/trip/" + trip_id + "/comments",
				data: {'text': reply_input.val(), 'parent': id},
				success: function(result) {
					console.log('Successful post');
					console.log(result);
					
				},
				error: function(result) {
					console.log('Error with POST');
					console.log(result)
				}
			})
		}
	});
	
	root_elem.after(reply_input);
	reply_input.after(reply_btn);
	
	return reply_input;
}