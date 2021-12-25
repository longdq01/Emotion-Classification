// tạo tên thiết bị a - Kíp b
$(document).ready(function () {
    var name = undefined;
    var kip = undefined;
    $("#device").change(function () {
        name = $("#device option:selected").val();
        alert("Bạn đang chọn thiết bị " + name);
        if (kip != undefined) {
            const template = `Thiết bị ${name} - Kíp ${kip}`;
            $("#informleft").html(template);
            $("#informright").html(template);
        }
        else {
            const template = `Thiết bị ${name}`;
            $("#informleft").html(template);
            $("#informright").html(template);
        }
    });

    $("#shift").change(function () {
        kip = $("#shift option:selected").val();
        alert("Bạn đang chọn kíp " + kip);
        if (name != undefined) {
            const template = `Thiết bị ${name} - Kíp ${kip}`;
            $("#informleft").html(template);
            $("#informright").html(template);
        }
        else {
            const template = `Kip ${kip}`;
            $("#informleft").html(template);
            $("#informright").html(template);
        }
    });

    $("#setstt").click(function () {
        const template = undefined
        $("#informleft").html("Thiết bị - kíp");
        $("#informright").html("Thiết bị - kíp");
    });
});