var keyEvents = [];

function keyPressEvent(e, downOrUp) {
  var press = (e.which) ? e.which : e.presskeys;
  keyEvents.push([window.performance.now(), press, downOrUp]);
}

function printKeyEvents() {
  document.getElementById("output").innerHTML = JSON.stringify(keyEvents);
}
