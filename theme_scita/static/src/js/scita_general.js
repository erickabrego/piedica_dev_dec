// Owl slider
odoo.define('theme_scita.scita_general_js', function(require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    // for megamenu  menu_style_3
    // var ajax = require('web.ajax');

        // $(".cc-cookies .btn-primary").click(function(e) {
        //     e.preventDefault();
        //     ajax.jsonRpc('/scita_cookie_notice/ok', 'call').then(function (data) {
        //         if (data.result == 'ok') {
        //             $(e.target).closest(".cc-cookies").hide("fast");
        //         }
        //     });
        // });
    
    
    $(document).on('click', '.li-mega-menu', function(e) {
        e.stopPropagation()
    });
    //End megamemu
     $(document).ready(function(){
        if ($('div').hasClass("o_offcanvas_menu_backdrop")){
            $(".o_offcanvas_menu_backdrop").parent().addClass("sct_off_canvas");
        }
        $(window).trigger('scroll');
        //mobile filter overlay script
        $('.sct_btm_mobile .btn-link').on("click",function() {
            $('.sct_shop_box').addClass("sct_shop_box_overlay");
        });
        $('.sct_filter_close').on("click",function() {
            $('.sct_shop_box').removeClass("sct_shop_box_overlay");
        });
        if ($('button').hasClass("sct_btm_mobile_btn")){
            $('#wrapwrap').addClass("sct-mobile-pro-list");
        }

        $('li.position-static').mouseenter(
            function(){ 
                if ($("div.o_mega_menu_container_size").length==0)
                {
                    $(this).parent().addClass('full-size-megamenu');
                    $(this).parent().closest('div.container').css("position", "static");
                }
                else
                {
                    $(this).parent().addClass('container-size-megamenu');
                    $(this).parent().closest('div.container').css("position", "relative");
                    
                }
            }
        )
        $('li.position-static').mouseleave(
            function(){ 
                if ($("div.o_mega_menu_container_size").length==0)
                {
                    $(this).parent().removeClass('full-size-megamenu');
                    $(this).parent().closest('div.container').css("position", "relative");
                }
                else
                {
                   $(this).parent().removeClass('container-size-megamenu');
                   $(this).parent().closest('div.container').css("position", "relative");

                }
            }
        )
        $('li.position-static').addClass('li-mega-menu');
        $('li.position-static').removeClass('dropdown');
        $('li.position-static div').addClass('mega-dropdown-menu');
        // for accordion 2 snippets 

        $("section.accordion_v_2 a.card-header").click(function(e) {
             $(this).parent().toggleClass('active');
        });
        // recommended_products_slider
        $('div#recommended_products_slider').owlCarousel({
            margin: 20,
            responsiveClass: true,
            items: 4,
            rtl: _t.database.parameters.direction === 'rtl',
            // loop: true,
            autoPlay: 7000,
            stopOnHover: true,
            navigation: true,
            responsive: {
                0: {
                    items: 1,
                },
                500: {
                    items: 2,
                },
                700: {
                    items: 3,
                },
                1000: {
                    items: 4,
                },
                1500: {
                    items: 4,
                }
            }
        });
            // Grid/List switching code
        $(".oe_website_sale .shift_list_view").click(function(e) {
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(".oe_website_sale .shift_2_col_grid_view").removeClass('active');
            $(".oe_website_sale .shift_4_col_grid_view").removeClass('active');
            $(this).addClass('active');
            $('#products_grid').addClass("list-view-box");
            $('.oe_website_sale .oe_subdescription').removeClass('o_hidden');
            localStorage.setItem("product_view", "list");
            pimgheight();
        });

        $(".oe_website_sale .shift_grid_view").click(function(e) {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(".oe_website_sale .shift_2_col_grid_view").removeClass('active');
            $(".oe_website_sale .shift_4_col_grid_view").removeClass('active');
            $(this).addClass('active');
            $(".oe_website_sale .grid_column").removeClass('col-md-6');
            $(".oe_website_sale .grid_column").removeClass('col-md-3');
            $(".oe_website_sale .grid_column").addClass('col-md-4');
            $('#products_grid').removeClass("list-view-box");
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
            localStorage.setItem("product_view", "grid");
            pimgheight();
        });
        $(".oe_website_sale .shift_2_col_grid_view").click(function(e) {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(".oe_website_sale .shift_4_col_grid_view").removeClass('active');
            $(this).addClass('active');
            $(".oe_website_sale .grid_column").removeClass('col-md-4');
            $(".oe_website_sale .grid_column").removeClass('col-md-3');
            $(".oe_website_sale .grid_column").addClass('col-md-6');
            $('#products_grid').removeClass("list-view-box");
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
            localStorage.setItem("product_view", "2-grid");
            pimgheight();
        });
        $(".oe_website_sale .shift_4_col_grid_view").click(function(e) {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(".oe_website_sale .shift_2_col_grid_view").removeClass('active');
            $(this).addClass('active');
            $(".oe_website_sale .grid_column").removeClass('col-md-4');
            $(".oe_website_sale .grid_column").removeClass('col-md-6');
            $(".oe_website_sale .grid_column").addClass('col-md-3');
            $('#products_grid').removeClass("list-view-box");
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
            localStorage.setItem("product_view", "4-grid");
            pimgheight();
        });
        

        if (localStorage.getItem("product_view") == 'list') {
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(".oe_website_sale .shift_list_view").addClass('active');
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
            $('#products_grid').addClass("list-view-box");
            $(".oe_website_sale .grid_column").removeClass('col-md-3');
            $(".oe_website_sale .grid_column").removeClass('col-md-6');
            $(".oe_website_sale .grid_column").addClass('col-md-4');
            $('.oe_website_sale .oe_subdescription').removeClass('o_hidden');
        }

        if (localStorage.getItem("product_view") == 'grid') {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(".oe_website_sale .shift_grid_view").addClass('active');
            $('.oe_website_sale .oe_subdescription').removeClass('o_hidden');
            $('#products_grid').removeClass("list-view-box");
            $(".oe_website_sale .grid_column").removeClass('col-md-3');
            $(".oe_website_sale .grid_column").removeClass('col-md-6');
            $(".oe_website_sale .grid_column").addClass('col-md-4');
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
        }
        if (localStorage.getItem("product_view") == '2-grid') {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(".oe_website_sale .shift_2_col_grid_view").addClass('active');
            $('.oe_website_sale .oe_subdescription').removeClass('o_hidden');
            $('#products_grid').removeClass("list-view-box");
            $(".oe_website_sale .grid_column").removeClass('col-md-4');
            $(".oe_website_sale .grid_column").removeClass('col-md-3');
            $(".oe_website_sale .grid_column").addClass('col-md-6');
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
        }
        if (localStorage.getItem("product_view") == '4-grid') {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(".oe_website_sale .shift_2_col_grid_view").removeClass('active');
            $(".oe_website_sale .shift_4_col_grid_view").addClass('active');
            $('.oe_website_sale .oe_subdescription').removeClass('o_hidden');
            $('#products_grid').removeClass("list-view-box");
            $(".oe_website_sale .grid_column").removeClass('col-md-4');
            $(".oe_website_sale .grid_column").removeClass('col-md-6');
            $(".oe_website_sale .grid_column").addClass('col-md-3');
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
        }

            var videoSrc;  
            $('.static-youtube').on('click',function() {
                event.preventDefault();
                videoSrc = $(this).attr('href');
               
                if(videoSrc)
                {
                    var convt_embed = videoSrc.replace("watch?v=", "embed/");    
                    
                    $('#youtube_id').attr('data',convt_embed)
                }
                
            });
            // $('section#adv_banner').masonry({rowMinAspectRatio: 3.3, borderWidth: 4});
            var offset = 300,
            //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
            offset_opacity = 1200,
            //duration of the top scrolling animation (in ms)
            scroll_top_duration = 700,
            //grab the "back to top" link
            $back_to_top = $('.cd-top');

            //hide or show the "back to top" link
            $('#wrapwrap').on('scroll',function() {
                ($(this).scrollTop() > offset) ? $back_to_top.addClass('cd-is-visible'): $back_to_top.removeClass('cd-is-visible cd-fade-out');
                if ($(this).scrollTop() > offset_opacity) {
                    $back_to_top.addClass('cd-fade-out');
                }
            });

            
            //smooth scroll to top
            $back_to_top.on('click', function(event) {
                event.preventDefault();
                $('body,html').animate({scrollTop: 0}, scroll_top_duration);
            });
            if($(".oe_website_sale").length === 0){
                $("div#wrap").addClass("oe_website_sale");
            }
            if($(".js_cart_summary").length === 0){
                $("div.oe_cart").removeClass("col-xl-8");
            }
            else
            {
             $("div.oe_cart").addClass("col-xl-8");   
            }
            //scroll top end
            //number slider count start
                var totalItems = $('.myNumCarousel .carousel-item').length;
                var currentIndex_active = $('.myNumCarousel  div.carousel-item.active').index() + 1;

                var down_index=currentIndex_active;
                $('.myNumCarousel .num').html(''+currentIndex_active+'/'+totalItems+'');
                $(".myNumCarousel .carousel-control-next").on('click',function(){
                    currentIndex_active = $('.myNumCarousel div.carousel-item.active').index() + 2;
                    if (totalItems >= currentIndex_active)
                    {
                        down_index= $('.myNumCarousel div.carousel-item.active').index() + 2;
                        $('.myNumCarousel .num').html(''+currentIndex_active+'/'+totalItems+'');
                    }
                    if (totalItems<currentIndex_active)
                    {   
                        var currentIndex_active = currentIndex_active - totalItems;
                        $('.myNumCarousel .num').html(''+currentIndex_active+'/'+totalItems+'');
                    }
                });
                $(".myNumCarousel .carousel-control-prev").on('click',function(){
                    down_index=down_index-1;
                    if (down_index >= 1 )
                    {
                        $('.myNumCarousel .num').html(''+down_index+'/'+totalItems+'');
                    }
                    if(down_index <= 0)
                    {
                        down_index=totalItems;
                        $('.myNumCarousel .num').html(''+down_index+'/'+totalItems+'');
                    }
                });
            //number slider count End
        // Price slider code start
        var minval = $("input#m1").attr('value'),
            maxval = $('input#m2').attr('value'),
            minrange = $('input#ra1').attr('value'),
            maxrange = $('input#ra2').attr('value'),
            website_currency = $('input#scita_website_currency').attr('value');
        if (!minval) {
            minval = 0;
        }
        if (!maxval) {
            maxval = maxrange;
        }
        if (!minrange) {
            minrange = 0;

        }
        if (!maxrange) {
            maxrange = 2000;
        }

        $("div#priceslider").ionRangeSlider({
            keyboard: true,
            min: parseInt(minrange),
            max: parseInt(maxrange),
            type: 'double',
            from: minval,
            to: maxval,
            step: 1,
            prefix: website_currency,
            grid: true,
            onFinish: function(data) {
                $("input[name='min1']").attr('value', parseInt(data.from));
                $("input[name='max1']").attr('value', parseInt(data.to));
                $("div#priceslider").closest("form").submit();
            },
        });
        // Price slider code ends
        $('a.static-youtube').on('click', function(e) {
            $('.data-youtube').removeClass("o_hidden");
        });

        $('li.menu_style_3').on('click', function(e) {
                equal_height_prod();
        });
        equal_height_all();
        setTimeout(function(){
            $('.o_extra_menu_items .dropdown-menu').css('display','none');
            $('li.o_extra_menu_items .dropdown').on('click',function(event) {
                event.stopPropagation();
                $(this).find('.dropdown-menu').slideToggle();

            });
            $('li.o_extra_menu_items li.li-mega-menu').on('click',function(event) {
                event.stopImmediatePropagation();
                $(this).find('.dropdown-menu').slideToggle();

            });
            var sliderTwo = $('.mm-slider .carousel').carousel({
                /* your options for slider #2 */
            })

            $(".mm-slider .carousel-control div").click(function (e) {
                var index = $(this).data('slide');
                sliderTwo.carousel(index);
                e.preventDefault();
            });
        },100);
    });
    $(document).on('click',function (e){
       $('span#close_youtube_bar').on('click', function(e) {
            $('.data-youtube').addClass("o_hidden");
        });
    }); 

    function equal_height_prod() {
        function resetHeightReddy() {
            var maxHeight = 0;
            
                $("span.sct-pro-menu-name").height("auto").each(function() {
                    maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
                }).height(maxHeight);
            

        }
        resetHeightReddy();
        $(window).resize(function() {
            resetHeightReddy();
        });
    }
    
    function equal_height_all() {
        function resetHeight() {
            var maxHeight = 0;
            $(".it-icon h4").height("auto").each(function() {
                maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
            }).height(maxHeight);
            $(".myourteam .image-container").height("auto").each(function() {
                maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
            }).height(maxHeight);
            $(".it_blogs .blog-thumb").height("auto").each(function() {
                maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
            }).height(maxHeight);
            $(".case_study_varient_2 .case_study_box").height("auto").each(function() {
                maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
            }).height(maxHeight);
        }
        resetHeight();
        $(window).resize(function() {
            resetHeight();
        });
    }
    function truncateText(selector, maxLength) {
        var element = document.querySelector(selector),
            truncated = element.innerText;

        if (truncated.length > maxLength) {
            truncated = truncated.substr(0,maxLength) + '...';
        }
        return truncated;
    }
    
    // product equal size thumb
    $(document).ready(pimgheight);
    $(window).on('resize',pimgheight);
    function pimgheight() {
        var divWidth = $('.cs-product .pwp-img a').width(); 
        $('.cs-product .pwp-img a').height(divWidth);
    }
     $("li#edit-page-menu").on('click',function(){
        waitForElementToDisplay("div#scita_snippets",1000);
    });
    function waitForElementToDisplay(selector, time) {
        if(document.querySelector(selector)!=null) {
            $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
            $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

            $("select#selSnippetCat").on('change',function(){
                if($("select#selSnippetCat").val()=='banner')
                {
                    $("#scita_snippets [data-disp=banner]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='newsletter')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='deal_days')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='blog')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='our_team')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='testimonial')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='service')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='portfolio')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='advbanner')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='pricing_table')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='trust_icon')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='contact_us')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='how_it_works')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='statistics')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='content_block')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='client_snippet')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='category_snippet')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='case_study')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='brand')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='about_us')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='accordion')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='timeline')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='timeline')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='multi_product')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp1=multi_product]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");

                }
                else if($("select#selSnippetCat").val()=='google_map_snippet')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().removeClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().addClass("o_hidden");
                }
                else if($("select#selSnippetCat").val()=='html_builder')
                {
                    $("#scita_snippets [data-disp=banner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=newsletter]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=deal_days]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=blog]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=our_team]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=testimonial]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=service]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=portfolio]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=advbanner]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=pricing_table]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=trust_icon]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=contact_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=how_it_works]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=statistics]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=content_block]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=client_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=category_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=case_study]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=brand]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=about_us]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=accordion]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=timeline]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=multi_product]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=google_map_snippet]").parent().addClass("o_hidden");
                    $("#scita_snippets [data-disp=html_builder]").parent().removeClass("o_hidden");
                }
            });
            return;
        }
        else {
            setTimeout(function() {
                waitForElementToDisplay(selector, time);
            }, time);
        }
    }
});