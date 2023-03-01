let elements = document.querySelectorAll('.floor2');
let lastClicked = elements[0];

$(document).ready(function () {
    $('#selectroom').change(function () {
        var value = $(this).val();
        ActiveRoom(document.getElementById(value), 1);
        console.log("выбран кабинет " + value);
    });
});

for (let i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', function () {
        ActiveRoom(this, 0);
        $('#selectroom').val(this.getAttribute("id"));
        $('#selectroom').select2();
    });
}

function ActiveRoom(el, mode) {
    if (!el.classList.contains('closed')) {

        lastClicked.classList.remove('active');
        el.classList.add('active');
        pointerElem = document.getElementById('menuchosed');
        nav = document.getElementById('nav');
        if (mode == 0) { // через карту
            var mouseX = event.pageX+1;
            console.log(event.pageX)
            var mouseY = event.pageY-30;
        } else if (mode == 1) { // через поиск
            //console.log("getBoundingClientRect() " + el.getBoundingClientRect());
            let box = el.getBoundingClientRect();
            //console.log(box);
            //console.log(box.top + window.pageYOffset)
            var mouseX = box.left + window.pageXOffset+15;
            var mouseY = box.top + window.pageYOffset;
        }
        pointerElem.style.left = Math.floor(mouseX) + 'px';
        console.log(pointerElem.style.left)
        //console.log("pointerElem.style.left " + pointerElem.style.left);
        //console.log("mouseX " + mouseX);
        //console.log("mouseY " + mouseY);
        //console.log("nav.offsetHeight " + nav.offsetHeight);
        pointerElem.style.top = Math.floor(mouseY) + 'px';
        pointerElem.style.display = 'block'
        document.getElementById('menu').style.display = 'none';
        document.getElementById('chosedroom_confirm').innerHTML = el.getAttribute("id");
        document.getElementById('chosedroom_confirm').classList.remove('hidden_step');
        document.querySelector('#btn_step2a').disabled = false;
        document.getElementById('textmenuchosed').innerHTML = el.getAttribute("id");
        document.getElementById('id_room').value = el.getAttribute("id");
        lastClicked = el;
    }
}

elements.forEach(el => {
    el.addEventListener('mouseover', () => {
        if (!el.classList.contains('active') && !el.classList.contains('closed')) {
            document.getElementById('menu').style.display = 'block'
            document.getElementById('textmenu').innerHTML = el.getAttribute("id");
        }
    })
})

elements.forEach(el => {
    el.addEventListener('mouseover', () => {
        if (el.classList.contains('closed')) {
            pointerElem = document.getElementById('menuclosed');
            var mouseX = event.pageX;
            var mouseY = event.pageY;
            pointerElem.style.left = Math.floor(mouseX + 1) + 'px';
            pointerElem.style.top = Math.floor(mouseY - 30) + 'px';
            document.getElementById('menuclosed').style.display = 'block'
            document.getElementById('textmenuclosed').innerHTML = "Ключ забрал Иванов И.И.";
        }
    })
})

elements.forEach(el => {
    el.addEventListener('mouseout', () => {
        document.getElementById('menu').style.display = 'none';
        document.getElementById('menuclosed').style.display = 'none';
    })
})

$(document).ready(function () {
    $('.js-select2').select2({
        placeholder: "Выберите кабинет",
        maximumSelectionLength: 2,
        language: "en"
    });
});

