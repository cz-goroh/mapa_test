function checkWorkerAndPushManager () {
    if (!('serviceWorker' in navigator)) {
        console.log('Workers are not supported.');
        return;
    }
    if (!('PushManager' in window)) {
        console.log('Push notifications are not supported.');
        return;
    }
}

function registerWorker () {
	window.addEventListener('load', function () {
        navigator.serviceWorker.register('/static/Order/js/sw.js').then(function (registration) {
            console.log('ServiceWorker registration successful');
        }, function (err) {
            console.log('ServiceWorker registration failed: ', err);
            return;
        });
    });
	return true;
}
var supported = checkWorkerAndPushManager();

if (supported){
        var worker = registerWorker ();
}
if (!('serviceWorker' in navigator)) {
    console.log('Workers are not supported.');
    return;
}
