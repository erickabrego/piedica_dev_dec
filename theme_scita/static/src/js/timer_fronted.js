odoo.define('theme_scita.front_js',function(require){
	'use strict';
  var sAnimation = require('website.content.snippets.animation');
  var ajax = require("web.ajax");
  
  sAnimation.registry.js_counter_timer = sAnimation.Class.extend({
    selector : ".js_counter_timer",
    disabledInEditableMode: true,
    start: function(){
        this.redrow();
      },
      stop: function(){
        this.clean();
      },

      redrow: function(debug){
        this.clean(debug);
        this.build(debug);
      },

      clean:function(debug){
        this.$target.empty();
      },
      build: function(debug)
      {
    	  
    	  var self = this;
    	  var date = self.$target.data("date");
    	  if(date != "nan")
        	  {
    		  var toDate = new Date(date).getTime();
    		  var x = setInterval(function() {
    				
    				// Get todays date and time
    				var now = new Date().getTime();
    				
    				// Find the diffrence between now an the count down date
    				var diffrence = toDate - now;// Time calculations for days, hours, minutes and seconds
    				
    				
    				if (diffrence > 0) {
    						var days = Math.floor(diffrence / (1000 * 60 * 60 * 24));
    						var hours = Math.floor((diffrence % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    						var minutes = Math.floor((diffrence % (1000 * 60 * 60)) / (1000 * 60));
    						var seconds = Math.floor((diffrence % (1000 * 60)) / 1000);
    						
    						if ((seconds+'').length == 1) {
    							seconds = "0" + seconds;
    						}
    						if ((days+'').length == 1) {
    							days = "0" + days;
    						}
    						if ((hours+'').length == 1) {
    							hours = "0" + hours;
    						}
    						if ((minutes+'').length == 1) {
    							minutes = "0" + minutes;
    						}
    				
    				}
    				// If the count down is over, write some text
    				if (diffrence <= 0) 
    				{
    					clearInterval(x);
    					seconds = "00" ;
    					days = "00";
    					minutes = "00";
    					hours = "00";
                        self.$target.addClass("time_out");
    					self.$target.append("<div class='time_over_msg'><p>"+self.$target.data("msg")+"</p></div>");
    				}
                    else
                    {   
                        self.$target.removeClass("time_out");
                    }
    				 
    				
    				if(self.$target.find(".counter_timer_div"))
    				{
						self.$target.find(".counter_timer_div").remove()
						var append_data="<div class='counter_timer_div'><span class='col-lg-3 col-md-3 col-sm-3 col-3 text-center'><div class='box_degit'><span id='days' class='d-count  t_days_hr_min_sec_digit o_default_snippet_text'>"+	days +"</span><span id='day_lbl' class='d-block'>DAYS</span></div></span><span class='col-lg-3 col-md-3 col-sm-3 col-3 text-center'><div class='box_degit'><span id='hours' class='d-count  t_days_hr_min_sec_digit o_default_snippet_text'>"+hours+"</span><span id='h_lbl' class='d-block'>HOURS</span></div></span><span class='col-lg-3 col-md-3 col-sm-3 col-3 text-center'><div class='box_degit'><span id='minutes' class='d-count t_days_hr_min_sec_digit o_default_snippet_text'>"+minutes+"</span><span id='m_lbl' class=' d-block'>MINS</span></div></span><span class='col-lg-3 col-md-3 col-sm-3 col-3 text-center'><div class='box_degit'><span id='seconds' class='d-count t_days_hr_min_sec_digit o_default_snippet_text'>"+seconds+"</span><span id='s_lbl' class='d-block'>SECS</span></div></span></div>";
						self.$target.find(".counter_timer_div").css("display","block")
                        self.$target.append(append_data)	
					}
    				}
                    , 1000);
        	   }	  
      }
  });
});
			
