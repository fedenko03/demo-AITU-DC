const StyleTop = 165;
const StyleLeft = 25;
const StyleRight = 330;
const RightMostWidth = 300;

$('#btn_step2a').prop('disabled', true);

        let elementsRoom = document.querySelectorAll('.roomFilling');
        let lastClickedRoom = elementsRoom[0];

        $(document).ready(function () {
            $('.js-select2').select2({
                placeholder: "Выберите кабинет",
                maximumSelectionLength: 2,
                language: "en"
            });


            $(document).ready(function () {
                $('#selectroom').change(function () {
                    var value = $(this).val();
                    mapElem = document.getElementById(value);

                    document.getElementById('InfoTable').style.display = 'none';
                    if (mapElem) {

                        lastClickedRoom.classList.remove('active');
                        mapElem.classList.add('active');
                        lastClickedRoom = mapElem;
                    }
                    var selectedOption = $(this).find(':selected');
                    document.getElementById('chosedroom_confirm').innerHTML = selectedOption.text();
                    document.getElementById('chosedroom_confirm').classList.remove('hidden_step');
                    document.getElementById('id_room').value = selectedOption.text();
                    $('#btn_step2a').prop('disabled', false);
                });
            });

        });




        const select = document.getElementById('floorSelect');
        const svg1 = document.getElementById('firstFloor');
        const svg2 = document.getElementById('secondFloor');
        const svg3 = document.getElementById('thirdFloor');

        select.addEventListener('change', () => {
            let floor = '1';
            const sign = document.getElementById('InfoTable')
            if (select.value === '1') {
                sign.style.display = 'none';
                floor = '1';
                svg1.style.display = 'block';
                svg2.style.display = 'none';
                svg3.style.display = 'none';
            } else if (select.value === '2') {
                sign.style.display = 'none';
                floor = '2';
                svg1.style.display = 'none';
                svg2.style.display = 'block';
                svg3.style.display = 'none';
            } else if (select.value === '3') {
                sign.style.display = 'none';
                floor = '3';
                svg1.style.display = 'none';
                svg2.style.display = 'none';
                svg3.style.display = 'block';
            }

            let elementsRoom1 = document.querySelectorAll('.roomFilling');
            for (let i = 0; i < elementsRoom1.length; i++) {
                elementsRoom1[i].classList.remove('unavailable', 'closed', 'dbExist');
                //console.log(elementsRoom1[i])
            }

            $.ajax({
                url: `${location.protocol}//${location.host}/main/get_rooms_floor/`,
                data: {
                    'floor': floor
                },
                dataType: 'json',
                success: function (data) {
                    //console.log(data)
                    for (let i = 0; i < data.rooms_list.length; i++) {
                        let elem1 = document.getElementById(data.rooms_list[i].map_id)
                        if (elem1) {
                            if (!data.rooms_list[i].is_visible) {
                                elem1.classList.add('unavailable');
                            } else if (data.rooms_list[i].is_occupied) {
                                elem1.classList.add('closed');
                            }
                            elem1.classList.add('dbExist');
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


        for (let i = 0; i < elementsRoom.length; i++) {
            elementsRoom[i].addEventListener('click', function (event) {
                if (!this.classList.contains('closed') && !this.classList.contains('unavailable') && this.classList.contains('dbExist')) {


                    const sign = document.getElementById('InfoTable')
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
                                lastClickedRoom.classList.remove('active');
                                elementsRoom[i].classList.add('active');
                                lastClickedRoom = elementsRoom[i];
                                document.getElementById('InfoTableAddit').textContent = 'СВОБОДНО';
                                sign.style.backgroundColor = '#249f38';
                                sign.style.borderColor = '#176d25';
                                idRoomTable.style.color = '#065914';
                                document.getElementById('chosedroom_confirm').innerHTML = data.room_map_info.name;
                                document.getElementById('chosedroom_confirm').classList.remove('hidden_step');
                                document.getElementById('id_room').value = data.room_map_info.name;

                                $('#btn_step2a').prop('disabled', false);
                                $('#selectroom').val(data.room_map_info.map_id);
                                $('#selectroom').select2();
                            } else {
                                for (let i = 0; i < data.room_map_info.role.length; i++) {
                                    let object = document.createElement('span');
                                    object.innerHTML = `<span class="badge bg-danger"
                                          style="font-weight: normal !important; font-size: 9px;padding-bottom: 2px;margin-bottom: 0px;margin-right: 2px;">${data.room_map_info.role[i]}</span>`
                                    document.getElementById('InfoTableRoom').appendChild(object);
                                }
                                document.getElementById('InfoTableAddit').textContent = 'ЗАНЯТО пользователем ' + data.room_map_info.user_fullname;
                                sign.style.backgroundColor = '#b42929';
                                sign.style.borderColor = 'rgb(222,13,0)';
                                idRoomTable.style.color = 'rgb(147,27,20)';
                            }
                            document.getElementById('idRoomTable').textContent = elementsRoom[i].id;
                        }
                    });


                    const x = event.clientX;
                    const y = event.clientY;


                    sign.style.position = 'absolute'
                    var container = document.getElementById('content')
                    var containerRect = container.getBoundingClientRect(); // get the container's position and size
                    sign.style.top = (event.clientY - containerRect.top - StyleTop) + 'px'; // set the top position relative to the container
                    sign.style.left = (event.clientX - containerRect.left - StyleLeft) + 'px'; // set the left position relative to the container
                    let idRoomTable = document.getElementById('idRoomTable')
                    idRoomTable.textContent = 'id:' + elementsRoom[i].id;
                    sign.style.borderBottomLeftRadius = "0px";
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


                    const sign = document.getElementById('InfoTable')
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
                                sign.style.backgroundColor = '#249f38';
                                sign.style.borderColor = '#176d25';
                                idRoomTable.style.color = '#065914';
                                document.getElementById('InfoRoles').style.color = 'rgb(23 58 15)';

                                document.getElementById('chosedroom_confirm').innerHTML = data.room_map_info.name;
                                document.getElementById('chosedroom_confirm').classList.remove('hidden_step');
                                document.getElementById('id_room').value = data.room_map_info.name;
                                $('#btn_step2a').prop('disabled', false);
                                $('#selectroom').val(data.room_map_info.map_id);
                                $('#selectroom').select2();
                            } else {
                                for (let i = 0; i < data.room_map_info.role.length; i++) {
                                    let object = document.createElement('span');
                                    object.innerHTML = `<span class="badge bg-danger"
                                          style="font-weight: normal !important; font-size: 9px;padding-bottom: 2px;margin-bottom: 0px;margin-right: 2px;">${data.room_map_info.role[i]}</span>`
                                    document.getElementById('InfoTableRoom').appendChild(object);
                                }
                                document.getElementById('InfoTableAddit').textContent = 'ЗАНЯТО пользователем ' + data.room_map_info.user_fullname;
                                sign.style.backgroundColor = '#e03e3e';
                                sign.style.borderColor = 'rgb(222,13,0)';
                                idRoomTable.style.color = 'rgb(147,27,20)';
                            }
                            document.getElementById('idRoomTable').textContent = elementsRoom[i].id;
                        }
                    });


                    const x = event.clientX;
                    const y = event.clientY;


                    sign.style.position = 'absolute'
                    var container = document.getElementById('content')
                    var containerRect = container.getBoundingClientRect(); // get the container's position and size
                    sign.style.top = (event.clientY - containerRect.top - StyleTop) + 'px'; // set the top position relative to the container
                    sign.style.left = (event.clientX - containerRect.left - StyleLeft) + 'px'; // set the left position relative to the container
                    let idRoomTable = document.getElementById('idRoomTable')
                    idRoomTable.textContent = 'id:' + elementsRoom[i].id;
                    sign.style.borderBottomLeftRadius = "0px";
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
                                document.getElementById('InfoTableRoom').textContent = elementsRoom[i].id;

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
                    sign.style.backgroundColor = '#7a7979';
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
            });
        }