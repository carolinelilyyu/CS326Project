// Handles loading and replying to comments. Retrieves comments for given trip id using AJAX.

var trip_id = 6;

$(document).ready(function(){
	console.log('Doc ready');
	$.ajax({
		type: "get",
		url: "http://localhost:8000/trip/6/comments",
		contentType: "application/json",
		success: function(data) {
			console.log('Received response');
			console.log(data);
			
			// mapping of comment ids to created html
			var comments = new Map();
			// list of ids of parent comments 
			var parent_ids = [];
			
			var comment_header = document.getElementById('comments-header');
			
			for (var i = 0; i < data.length; i++) {
				console.log('Elem ' + i + ' is ' + data[i].id);
				
				var div = document.createElement('div');
				div.setAttribute('id', 'comment-' + data[i].id);
				div.className = 'comment';
				div.style.backgroundColor = '#CCC';
				
				div.innerHTML = '<p>' + data[i].author_name + '<p>';
				
				// comment does not have a parent
				if (data[i].parent === 0) {
					parent_ids.push(data[i].id);
				} else {
					div.innerHTML = '<p>Replying to ' + data[i].parent + '</p>';
				}
				
				div.innerHTML = div.innerHTML + '<p>' + data[i].timestamp + '</p>' + '<p>' + data[i].text + '</p>';
				
				comments.set(data[i].id, div);
				console.log(comments.size);
				console.log(comments.get(data[i].id));
			}
			
			console.log('Parents are ' + parent_ids);
			// add comments that do not have a parent (replies will already have been chained)
			for (var i = 0; i < parent_ids.length; i++) {
				console.log('hey');
				comment_header.append(comments.get(parent_ids[i]));
			}
		},
		error: function(){
			console.log('AJAX error');
		}
	});
});
/*
var comments = document.getElementsByClassName('comment');
var reply_btns = document.getElementsByClassName('comment-reply-btn');

console.log('Found ' + reply_btns.length + ' buttons');

// note: I am not good at Javascript. Please feel free to revise (and better yet, tell me how I can make it better)
for (var i = 0; i < reply_btns.length; i++) {
	reply_btns[i].dataset.replied = 0;
	handleElement(i);
}
	/*reply_btns[i].dataset.index = i;
	console.log('Button created for comment ' + reply_btns[i].dataset.dataCommentId);

	reply_btns[i].onclick = function(e) {
		console.log('You clicked button for comment ' + e.target.dataset.index);
		var reply = document.createElement('div');
		reply.innerHTML = '<input type="text" placeholder="Comment" class="form-control" />';
		e.target.appendChild(reply);
	}
	
}

function onClickReply(comment_index) {
	console.log(comment_index);
	
}*/
/*
function handleElement(i) {
    reply_btns[i].onclick=function() {
		console.log('Comment ' + i + ' clicked. Replied = ' + reply_btns[i].dataset.replied);
		// check comment has not been replied to
		if (reply_btns[i].dataset.replied === '0') {
			reply_btns[i].dataset.replied = '1';
			var reply_div = document.createElement('div');
			var text_input = document.createElement('input');
			var send_btn = document.createElement('button');
			
			// have it send a post when clicked  TODO: USE DJANGO FORM
			send_btn.onclick = function() {
				console.log('User is sending ' + text_input.value);
			}
			
			reply_div.appendChild(text_input);
			reply_div.appendChild(send_btn);
			//reply.innerHTML = '<input type="text" placeholder="Comment" class="form-control" /><button type="button">Send</button>';
			
			comments[i].appendChild(reply_div);
		}
    };
}*/
