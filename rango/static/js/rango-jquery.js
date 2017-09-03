$(document).ready(function(){
    $('#about-btn').click(function(evevt){
        msg = $('#msg').html()
        msg = msg + '11'
        $('#msg').html(msg)
    });

    $("p").hover(function(){
        $(this).css('color', 'red');
    },
        function(){
        $(this).css('color', 'blue');
        });


});