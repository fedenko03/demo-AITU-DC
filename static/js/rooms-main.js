let elementsRoom = document.querySelectorAll('.roomFilling');
const select = document.getElementById('floorSelect');
const svg1 = document.getElementById('firstFloor');
const svg2 = document.getElementById('secondFloor');
const svg3 = document.getElementById('thirdFloor');

const StyleTop = 127;
const StyleLeft = 0;
const StyleRight = 300;
const RightMostWidth = 300;

select.addEventListener('change', () => {
    let floor = '1';
    const sign = document.getElementById('InfoTable')
    if (select.value === '1') {
        sign.style.display = 'none';
        floor = '1';
        document.getElementById('textLabelTable').textContent = 'Все кабинеты 1 этажа';
        svg1.style.display = 'block';
        svg2.style.display = 'none';
        svg3.style.display = 'none';
    } else if (select.value === '2') {
        sign.style.display = 'none';
        document.getElementById('textLabelTable').textContent = 'Все кабинеты 2 этажа';
        floor = '2';
        svg1.style.display = 'none';
        svg2.style.display = 'block';
        svg3.style.display = 'none';
    } else if (select.value === '3') {
        sign.style.display = 'none';
        document.getElementById('textLabelTable').textContent = 'Все кабинеты 3 этажа';
        floor = '3';
        svg1.style.display = 'none';
        svg2.style.display = 'none';
        svg3.style.display = 'block';
    }
    clearTableRooms()
    $.ajax({
        url: `${location.protocol}//${location.host}/main/get_rooms_floor/`,
        data: {
            'floor': floor
        },
        dataType: 'json',
        success: function (data) {
            //console.log(data)
            //console.log(data.rooms_list.length)
            for (let i = 0; i < data.rooms_list.length; i++) {
                fillTableRooms(data.rooms_list[i])
                //console.log(data.rooms_list[i].map_id)
                let elem1 = document.getElementById(data.rooms_list[i].map_id)
                //console.log("\n\n\nELEM: ")
                //console.log(elem1)

                if (elem1) {
                    if (!data.rooms_list[i].is_visible) {
                        //console.log("is not vis " + !data.rooms_list[i].is_visible)
                        elem1.classList.add('unavailable');
                    } else if (data.rooms_list[i].is_occupied) {
                        //console.log("is occ " + data.rooms_list[i].is_occupied)
                        elem1.classList.add('closed');
                    }
                    elem1.classList.add('dbExist');
                    //console.log("ELEM: ")
                    //console.log(elem1)
                }
            }
            let elementsRoom1 = document.querySelectorAll('.roomFilling');
            for (let i = 0; i < elementsRoom1.length; i++) {
                if (!elementsRoom1[i].classList.contains('dbExist')) {
                    elementsRoom1[i].classList.add('unavailable');
                }
            }
        }
    });
});

let lastClickedRoom = elementsRoom[0];

for (let i = 0; i < elementsRoom.length; i++) {
    elementsRoom[i].addEventListener('click', function (event) {
        if (!this.classList.contains('closed') && !this.classList.contains('unavailable') && this.classList.contains('dbExist')) {
            lastClickedRoom.classList.remove('active');
            this.classList.add('active');
            lastClickedRoom = this;


            $.ajax({
                url: `${location.protocol}//${location.host}/main/get_room_map/`,
                data: {
                    'room_map_id': elementsRoom[i].id
                },
                dataType: 'json',
                success: function (data) {
                    //console.log(data)
                    document.getElementById('InfoTableRoom').textContent = data.room_map_info.name + ' ';
                    document.getElementById('InfoTableDescr').textContent = data.room_map_info.description;
                    if (!data.room_map_info.is_occupied) {
                        for (let i = 0; i < data.room_map_info.role.length; i++) {
                            let object = document.createElement('span');
                            object.innerHTML = `<span class="badge bg-success"
                                          style="font-weight: normal !important; font-size: 9px;padding-bottom: 2px;margin-bottom: 0px;margin-right: 2px;">${data.room_map_info.role[i]}</span>`
                            document.getElementById('InfoTableRoom').appendChild(object);
                        }
                        document.getElementById('InfoTableAddit').textContent = 'СВОБОДНО';
                    } else {
                        for (let i = 0; i < data.room_map_info.role.length; i++) {
                            let object = document.createElement('span');
                            object.innerHTML = `<span class="badge bg-danger"
                                          style="font-weight: normal !important; font-size: 9px;padding-bottom: 2px;margin-bottom: 0px;margin-right: 2px;">${data.room_map_info.role[i]}</span>`
                            document.getElementById('InfoTableRoom').appendChild(object);
                        }
                        document.getElementById('InfoTableAddit').textContent = 'ЗАНЯТО пользователем ' + data.room_map_info.user_fullname;
                    }
                    document.getElementById('idRoomTable').textContent = elementsRoom[i].id;
                }
            });


            const x = event.clientX;
            const y = event.clientY;


            const sign = document.getElementById('InfoTable')
            sign.style.position = 'absolute'
            var container = document.getElementById('content')
            var containerRect = container.getBoundingClientRect(); // get the container's position and size
            sign.style.top = (event.clientY - containerRect.top - StyleTop) + 'px'; // set the top position relative to the container
            sign.style.left = (event.clientX - containerRect.left - StyleLeft) + 'px'; // set the left position relative to the container
            let idRoomTable = document.getElementById('idRoomTable')
            idRoomTable.textContent = 'id:' + elementsRoom[i].id;
            sign.style.borderBottomLeftRadius = "0px";
            sign.style.backgroundColor = '#249f38';
            sign.style.borderColor = '#176d25';
            idRoomTable.style.color = '#065914';
            sign.style.borderBottomRightRadius = "20px";
            sign.style.display = 'block';

            var viewportWidth = window.innerWidth;
            var signLeft = parseFloat(getComputedStyle(sign).left);
            var signWidth = parseFloat(getComputedStyle(sign).width);
            var rightmostPoint = signLeft + signWidth + RightMostWidth;
            if (rightmostPoint > viewportWidth) {
                sign.style.left = (event.clientX - containerRect.left - StyleRight) + 'px';
                sign.style.borderBottomLeftRadius = "20px";
                sign.style.borderBottomRightRadius = "0px";
            }

        } else if (this.classList.contains('closed')) {
            lastClickedRoom.classList.remove('active');
            this.classList.add('active');
            lastClickedRoom = this;


            $.ajax({
                url: `${location.protocol}//${location.host}/main/get_room_map/`,
                data: {
                    'room_map_id': elementsRoom[i].id
                },
                dataType: 'json',
                success: function (data) {
                    //console.log(data)
                    document.getElementById('InfoTableRoom').textContent = data.room_map_info.name + ' ';
                    document.getElementById('InfoTableDescr').textContent = data.room_map_info.description;
                    if (!data.room_map_info.is_occupied) {
                        for (let i = 0; i < data.room_map_info.role.length; i++) {
                            let object = document.createElement('span');
                            object.innerHTML = `<span class="badge bg-success"
                                          style="font-weight: normal !important; font-size: 9px;padding-bottom: 2px;margin-bottom: 0px;margin-right: 2px;">${data.room_map_info.role[i]}</span>`
                            document.getElementById('InfoTableRoom').appendChild(object);
                        }
                        document.getElementById('InfoTableAddit').textContent = 'СВОБОДНО';
                    } else {
                        for (let i = 0; i < data.room_map_info.role.length; i++) {
                            let object = document.createElement('span');
                            object.innerHTML = `<span class="badge bg-danger"
                                          style="font-weight: normal !important; font-size: 9px;padding-bottom: 2px;margin-bottom: 0px;margin-right: 2px;">${data.room_map_info.role[i]}</span>`
                            document.getElementById('InfoTableRoom').appendChild(object);
                        }
                        document.getElementById('InfoTableAddit').textContent = 'ЗАНЯТО пользователем ' + data.room_map_info.user_fullname;
                    }
                    document.getElementById('idRoomTable').textContent = elementsRoom[i].id;
                }
            });


            const x = event.clientX;
            const y = event.clientY;


            const sign = document.getElementById('InfoTable')
            sign.style.position = 'absolute'
            var container = document.getElementById('content')
            var containerRect = container.getBoundingClientRect(); // get the container's position and size
            sign.style.top = (event.clientY - containerRect.top - StyleTop) + 'px'; // set the top position relative to the container
            sign.style.left = (event.clientX - containerRect.left - StyleLeft) + 'px'; // set the left position relative to the container
            let idRoomTable = document.getElementById('idRoomTable')
            idRoomTable.textContent = 'id:' + elementsRoom[i].id;
            sign.style.borderBottomLeftRadius = "0px";
            sign.style.backgroundColor = '#e03e3e';
            sign.style.borderColor = 'rgb(222,13,0)';
            idRoomTable.style.color = 'rgb(147,27,20)';
            sign.style.borderBottomRightRadius = "20px";
            sign.style.display = 'block';

            var viewportWidth = window.innerWidth;
            var signLeft = parseFloat(getComputedStyle(sign).left);
            var signWidth = parseFloat(getComputedStyle(sign).width);
            var rightmostPoint = signLeft + signWidth + RightMostWidth;
            if (rightmostPoint > viewportWidth) {
                sign.style.left = (event.clientX - containerRect.left - StyleRight) + 'px';
                sign.style.borderBottomLeftRadius = "20px";
                sign.style.borderBottomRightRadius = "0px";
            }
        } else if (this.classList.contains('unavailable')) {
            lastClickedRoom.classList.remove('active');
            this.classList.add('active');
            lastClickedRoom = this;

            const x = event.clientX;
            const y = event.clientY;


            $.ajax({
                url: `${location.protocol}//${location.host}/main/get_room_map/`,
                data: {
                    'room_map_id': elementsRoom[i].id
                },
                dataType: 'json',
                success: function (data) {
                    //console.log(data)
                    if (!data.room_map_info) {
                        document.getElementById('InfoTableRoom').textContent = elementsRoom[i].id + ' ';
                        document.getElementById('InfoTableDescr').textContent = "Комнаты нет в Базе данных";
                        document.getElementById('InfoTableAddit').textContent = 'НЕДОСТУПНО';
                        document.getElementById('idRoomTable').textContent = elementsRoom[i].id;
                    } else {
                        document.getElementById('InfoTableRoom').textContent = data.room_map_info.name + ' ';
                        for (let i = 0; i < data.room_map_info.role.length; i++) {
                            let object = document.createElement('span');
                            object.innerHTML = `<span class="badge bg-secondary"
                                          style="font-weight: normal !important; font-size: 9px;padding-bottom: 2px;margin-bottom: 0px;margin-right: 2px;">${data.room_map_info.role[i]}</span>`
                            document.getElementById('InfoTableRoom').appendChild(object);
                        }
                        document.getElementById('InfoTableDescr').textContent = data.room_map_info.description;
                        if (!data.room_map_info.is_visible) {
                            document.getElementById('InfoTableAddit').textContent = 'ОТКЛЮЧЕНА в настройках';
                        }
                        document.getElementById('idRoomTable').textContent = elementsRoom[i].id;
                    }
                }
            });


            const sign = document.getElementById('InfoTable')
            sign.style.position = 'absolute'
            var container = document.getElementById('content')
            var containerRect = container.getBoundingClientRect(); // get the container's position and size
            sign.style.top = (event.clientY - containerRect.top - StyleTop) + 'px'; // set the top position relative to the container
            sign.style.left = (event.clientX - containerRect.left - StyleLeft) + 'px'; // set the left position relative to the container
            let idRoomTable = document.getElementById('idRoomTable')
            idRoomTable.textContent = 'id:' + elementsRoom[i].id;
            sign.style.borderBottomLeftRadius = "0px";
            sign.style.backgroundColor = '#9c9c9c';
            sign.style.borderColor = '#585858';
            idRoomTable.style.color = '#525050';
            sign.style.borderBottomRightRadius = "20px";
            sign.style.display = 'block';

            var viewportWidth = window.innerWidth;
            var signLeft = parseFloat(getComputedStyle(sign).left);
            var signWidth = parseFloat(getComputedStyle(sign).width);
            var rightmostPoint = signLeft + signWidth + RightMostWidth;
            if (rightmostPoint > viewportWidth) {
                sign.style.left = (event.clientX - containerRect.left - StyleRight) + 'px';
                sign.style.borderBottomLeftRadius = "20px";
                sign.style.borderBottomRightRadius = "0px";
            }
        }
        /*
        setTimeout(function () {
            document.getElementById('InfoTable').style.display = 'none';
        }, 10000)
         */
    });
}

function clearTableRooms() {
    let elementsRoom1 = document.querySelectorAll('.roomFilling');
    for (let i = 0; i < elementsRoom1.length; i++) {
        elementsRoom1[i].classList.remove('unavailable', 'closed', 'dbExist');
        //console.log(elementsRoom1[i])
    }

    let containerTableRooms = document.getElementById('tbodyRoom');
    let roomsLength = containerTableRooms.childNodes.length;
    while (roomsLength > 0) {
        containerTableRooms.removeChild(containerTableRooms.firstChild)
        roomsLength--
    }
}


function fillTableRooms(data) {
    let containerTableRooms = document.getElementById('tbodyRoom');
    let object = document.createElement('tr');
    object.innerHTML = `
            <td>${data.name}</td>
<td>${data.description}</td>
${data.is_occupied ? `<td class="text-danger">Занят</td>` : `<td class="text-success">Свободен</td>`}
<td>
  ${data.role_name_list ? data.role_name_list.map(role => `<span class="badge bg-primary">${role}</span>`).join(' ') : ''}
</td>
${!data.is_visible ? `<td class="text-danger">Скрыта</td>` : `<td class="text-success">Видна</td>`}

            `
    containerTableRooms.appendChild(object);
}