$(document).ready(function () {
    $(".overlay").click(function(){
        window.open($(this).find("a:first").attr("href"));
        return false;
    });

    $(".name_music").each(function (i) {
        if ($(this).prop('scrollHeight') > $(this).height()) {
            $(this).mouseover(function () {
                $(this).addClass("scroll-up");
            });
            $(this).mouseout(function () {
                $(this).removeClass("scroll-up");
            });
        }
    });

});