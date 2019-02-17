//$(document).ready(function() {
  //  $("#submit").attr("disabled", true);
    //$("#select").change(function(){
  //    if($("#select option:selected").val() != "")
  //    {
//        $("#submit").attr("disabled", false);
  //    }
  //  });
//});
$(document).ready(function() {
  console.log("testing");
  $("#submit").attr("disabled", true);
  $("#myInput").change(function(){
    var input = $("#myInput").val();
    console.log(jQuery.inArray(input, countriesArr));
    if(input.length > 0 && input != "Country" )
    {
      $("#submit").attr("disabled", false);
    }
  });
});
