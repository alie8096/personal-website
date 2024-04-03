// for admin-panel
$(document).ready(function() {
    $('.sidebar ul li a').click(function() {
        $(this).addClass('active').siblings().removeClass('active');
    });
});