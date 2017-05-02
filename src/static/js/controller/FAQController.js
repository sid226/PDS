myApp.controller('FAQController', function($scope){
    $(document).ready(function() {
        $('.page_header').html('<h3>&nbsp;</h3><a href="#/" id="search_link">Back To Search</a>');
        $('#back_to_top').click(function() {
            $('body,html').animate({scrollTop:0},"fast");
            window.location.href = "#/faq";
        });
    });

    var shouldShowLink = function(el) {
        var min_height = $(window).height();
        var go_to_top = $(window).scrollTop()+ 20;
        var where_to_go = $(el).offset().top;

        return where_to_go <= (min_height + go_to_top);
    }

    $(window).scroll(function() {
        if($(this).scrollTop() == 0) {
            $('#back_to_top').fadeOut();
        }else{
            $('#back_to_top').css('position','fixed');
            $('#back_to_top').fadeIn();
        }
    });
});