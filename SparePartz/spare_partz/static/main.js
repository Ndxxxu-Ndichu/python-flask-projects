$(document).ready(function() {
					
  $("#search").change(function(e) {
         hideAll();
              $(e.target.options).removeClass();
              var $selectedOption = $(e.target.options[e.target.options.selectedIndex]);
              $selectedOption.addClass('selected');
         $('#' + $selectedOption.val()).show();
  });
});

function hideAll() {
  $("#audio").hide();
  $("#brakes").hide();
  $("#engine").hide();
  $("#exterior").hide();
  $("#headlights").hide();
  $("#interior").hide();
  $("#motorcycle").hide();
  $("#safety").hide();
  $("#wheels").hide();
          
}