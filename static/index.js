/*Attempts to submit query when "enter" key is pressed*/
$(document).ready(function() {
    $('#myInput').keydown(function() {
        var message = $("input").val();
        if (event.keyCode == 13) {
            if (message == "") {
                alert("Enter Some Text In Textarea");
            } else {
                    $('#my_form').submit();
                    alert("Succesfully submitted:- " + message);
            }
            $("input").val('');
            return false;
        }
    });
});







