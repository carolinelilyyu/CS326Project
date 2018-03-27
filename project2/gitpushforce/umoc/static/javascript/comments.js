// Handles user replying to a comment

console.log('Found the file')

var comments = document.getElementsByClassName('comment');
var reply_btns = document.getElementsByClassName('comment-reply-btn');

console.log('Found ' + reply_btns.length + ' buttons');

// note: I am not good at Javascript. Please feel free to revise (and better yet, tell me how I can make it better)
for (var i = 0; i < reply_btns.length; i++) {
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
		var reply = document.createElement('div');
		reply.innerHTML = '<input type="text" placeholder="Comment" class="form-control" />';
        comments[i].appendChild(reply);
    };
}
