

(function () {
  'use strict';

  var boxElem = document.getElementById('box1');
  var pointerElem = document.getElementById('menu');

  function onMouseMove(event) {
    var mouseX = event.pageX;
    var mouseY = event.pageY;

    requestAnimationFrame(function movePointer() {
      pointerElem.style.left = Math.floor(mouseX + 1) + 'px';
      pointerElem.style.top = Math.floor(mouseY - 30) + 'px';

    });
  }

  function disablePointer() {
    pointerElem.style.left = '-500px';
    pointerElem.style.top = '-500px';
  }

  boxElem.addEventListener('mousemove', onMouseMove, false);
  boxElem.addEventListener('mouseleave', disablePointer, false);

})();

(function () {
  'use strict';

  var boxElem = document.getElementById('box1');
  var pointerElem = document.getElementById('menuclosed');

  function onMouseMove(event) {
    var mouseX = event.pageX;
    var mouseY = event.pageY;

    requestAnimationFrame(function movePointer() {
      pointerElem.style.left = Math.floor(mouseX + 1) + 'px';
      pointerElem.style.top = Math.floor(mouseY - 30) + 'px';

    });
  }

  function disablePointer() {
    pointerElem.style.left = '-500px';
    pointerElem.style.top = '-500px';
  }

  boxElem.addEventListener('mousemove', onMouseMove, false);
  boxElem.addEventListener('mouseleave', disablePointer, false);

})();

