odoo.define('theme_scita.see_more_brand_js', function(require) {
   "use strict";
    $(document).ready(function() {

        var size_li = $("#myList li").length;
        var x = 7;
        
        $('#myList li:lt('+x+')').show();
        $('#myList li').not(':lt('+x+')').hide();
        if (size_li > 7){
            $('a#loadMore').removeClass('o_hidden');
        }
        $('a#loadMore').click(function() {
            x= (x+5 <= size_li) ? x+5 : size_li;
            $('#myList li:lt('+x+')').show();
            $('a#showLess').removeClass('o_hidden');
            if (x == size_li){
                $('a#loadMore').addClass('o_hidden');
            }
        });
        $('a#showLess').click(function() {
            x=(x-5<0) ? 3 : x-5;
            $('#myList li').not(':lt('+x+')').hide();
            if (x <= 7){
                $('a#showLess').addClass('o_hidden');
                $('a#loadMore').removeClass('o_hidden');
            }
            if (x <= 7){
                $('#myList li:lt('+7+')').show();
            }
        });
    });

});