var button = document.getElementById("clickme"),
count = 0;
button.onclick = function () {
count++;
button.innerHTML = "Like " + count;
};

var button1 = document.getElementById("followme"),
count1 = 0;
button1.onclick = function () {
count1++;
button1.innerHTML = "follow " + count1;
};
var button2 = document.getElementById("post"),
count2 = 0;
button2.onclick = function () {
count2++;
button2.innerHTML = "post" + count2;
};