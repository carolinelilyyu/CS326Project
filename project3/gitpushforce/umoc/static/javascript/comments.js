// Handles user replying to a comment

console.log('Found the file')

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
}
