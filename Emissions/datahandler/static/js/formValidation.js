$(document).ready(function() {
  $("#submit").attr("disabled", true);
  $("#myInput").keypress(function(){
    var input = $("#myInput").val();
    checkIfValid(input);
  });
  $("body").click(function(){
    var input = $("#myInput").val();
    checkIfValid(input);
  });
});

function checkIfValid(input){
  console.log(input);
  var index = jQuery.inArray(input, countriesArr);
  console.log(index);
  console.log(countriesArr);
  if(input.length > 0 && input != "Country" && index !== -1)
  {
    $("#submit").attr("disabled", false);
  }
  else
  {
    $("#submit").attr("disabled", true);
  }
}
