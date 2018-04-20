/* Javascript adding Notification functionality (dismissing) */

console.log('Found notifications.js');

// click handlers for each dismiss-notification-btn
$('.dismiss-notification-btn').on('click', function() {
	var id = $(this).attr('id');
	console.log('clicked ' + id);
});