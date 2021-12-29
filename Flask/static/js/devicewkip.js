// tạo tên thiết bị a - Kíp b
$(document).ready(function () {
    $(".input-field").change(function () {
        cam_id = $("#device :selected").val();
        shift = $("#shift :selected").val();
        date = $("#start").val();
        emotion = $(".selected").attr("id");

        console.log(date, cam_id, shift, emotion)
        data = {}
        data['cameraId'] = cam_id;
        data['shift'] = shift;
        data['date'] = date;
        data['emotion'] = emotion;

        $.ajax({
            url: '/info',
            contentType: "application/json;charset=utf-8",
            dataType: 'json',
            type: "POST",
            data: JSON.stringify(data),
            success: function (response) {
                // console.log(response);
                var image = response['image'];
                $("#image").empty();
                for (img in image) {

                    // let src = 'https://image.shutterstock.com/image-photo/close-portrait-smiling-handsome-man-260nw-1011569245.jpg'
                    //let ele = `<div><img src = '${image[img]}' /></div>alt="img"></div>`;
                    let ele = `<div><img src = '${image[img]}' /></div>`;
                    $('#image').append(ele);
                }

                if (response['6'] == undefined) response['6'] = 0
                if (response['6'] == undefined) response['7'] = 0
                if (response['6'] == undefined) response['8'] = 0

                $("#useSmartPhone").text(response['6']);
                $("#useLaptop").text(response['7']);
                $("#other").text(response['8']);

                data = [];
                for (var i = 0; i < 6; i++) {
                    if (i.toString() in response)
                        data.push(response[i.toString()]);
                    else
                        data.push(0);
                }
                console.log(data)

                myChart.data.datasets[0].data = data;
                myChart.update();

            },
            error: function (error) {
                $("#wait-load").modal("hide");
                console.log(error);
            }
        });
    });

    // $("#setstt").click(function () {
    //     const template = undefined
    //     $("#informleft").html("Thiết bị - kíp");
    //     $("#informright").html("Thiết bị - kíp");
    // });

    var now = new Date();
    var month = (now.getMonth() + 1);
    var day = now.getDate();
    if (month < 10)
        month = "0" + month;
    if (day < 10)
        day = "0" + day;
    var today = now.getFullYear() + '-' + month + '-' + day;
    $('#start').val(today);

    $('#start').change(function () {
        var date = $(this).val();
        console.log(date, 'change')
    });

    $("#bar .emotion").click(function () {

        $("#bar .emotion").each(function () {
            $(this).removeClass("selected");
            $(this).css('border-bottom', 'none')
        });
        $(this).addClass("selected");
        $(this).css('border-bottom', '2px solid #2ecc71')

        cam_id = $("#device :selected").val();
        shift = $("#shift :selected").val();
        date = $("#start").val();
        emotion = $(".selected").attr("id");

        console.log(date, cam_id, shift, emotion)
        data = {}
        data['cameraId'] = cam_id;
        data['shift'] = shift;
        data['date'] = date;
        data['emotion'] = emotion;

        $.ajax({
            url: '/info',
            contentType: "application/json;charset=utf-8",
            dataType: 'json',
            type: "POST",
            data: JSON.stringify(data),
            success: function (response) {
                console.log(response);
                var image = response['image'];
                $("#image").empty();
                for (img in image) {

                    // let src = 'https://image.shutterstock.com/image-photo/close-portrait-smiling-handsome-man-260nw-1011569245.jpg'
                    //let ele = `<div><img src = '${image[img]}' /></div>alt="img"></div>`;
                    let ele = `<div><img src = '${image[img]}' /></div>`;
                    $('#image').append(ele);
                }

                if (response['6'] == undefined) response['6'] = 0
                if (response['6'] == undefined) response['7'] = 0
                if (response['6'] == undefined) response['8'] = 0

                $("#useSmartPhone").text(response['6'])
                $("#useLaptop").text(response['7'])
                $("#other").text(response['8'])

            },
            error: function (error) {
                $("#wait-load").modal("hide");
                console.log(error);
            }
        });
    });

});

