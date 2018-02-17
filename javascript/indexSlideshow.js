
data = ["people.jpg", "sunrise.jpg", "sunset.jpg"];
kTransitionTime = 3000;


// Python style format.
String.prototype.format = function() {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k]);
    }
    return a;
}

function swap(index) {
    let image_obj = document.querySelector('.center-image');
    image_obj.setAttribute('src', "images/" + String(data[index]));
    setTimeout(swap, kTransitionTime, (index + 1) % data.length);
}

setTimeout(swap, kTransitionTime, 0);
