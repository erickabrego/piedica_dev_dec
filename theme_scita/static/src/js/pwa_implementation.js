odoo.define('theme_scita.pwa_implementation_frontend_js', function(require) {
    'use strict';
    const isIos = () => {
      const userAgent = window.navigator.userAgent.toLowerCase();
      return /iphone|ipad|ipod/.test( userAgent );
    }

    const isInStandaloneMode = () => ('standalone' in window.navigator) && (window.navigator.standalone);

    if (isIos() && !isInStandaloneMode()) {
        var mobileDevicePopup = $(".mobile-deive-popup");
        mobileDevicePopup.show();
        $(mobileDevicePopup).click(function() {
            mobileDevicePopup.hide();
            localStorage.setItem("iphone_pwa_msg", 'false');
        });
    }
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service_worker').then(function(reg) {
        }).catch(function(error) {
        });
    }
    $(".sct_pwa_iphone_close").on('click',function(e) {
        $(e.target).closest(".mobile-deive-popup").hide("fast");
        localStorage.setItem("iphone_pwa_msg", 'false');
    });
    if (localStorage.getItem("iphone_pwa_msg") == 'false') {
        $(".mobile-deive-popup").addClass("o_hidden");
    }
});