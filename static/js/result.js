$(document).ready(function () {
  // Init
  $("#btn-predict").hide();
  $(".loader").hide();
  $("#result").hide();

  // for file name show
  $('input[type="file"]').change(function (e) {
    var filename1 = e.target.files[0].name;
    // console.log(filename1);
    $(".file-name").text(filename1);
  });

  function readURL(input) {
    if (input.files && input.files[0]) {
      $("#resimg").css("display", "flex");
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#resimg").attr("src", e.target.result);
        $(".wrapper").addClass("active");
        $("#cancel-btn i").click(function () {
          $("#resimg").attr("src", "");
          $(".wrapper").removeClass("active");
        });
        // $("#imagePreview").hide();
        // $("#imagePreview").fadeIn(650);
      };
      reader.readAsDataURL(input.files[0]);
    }
  }

  $("#default-btn").change(function () {
    // $(".image-section").show();
    $("#btn-predict").show();
    $("#result").text("");
    $("#result").hide();
    readURL(this);
  });

  // Predict
  $("#btn-predict").click(function () {
    var form_data = new FormData($("#upload-file")[0]);

    // Show loading animation
    $(this).hide();
    $(".loader").show();

    // Make prediction by calling api /predict
    $.ajax({
      type: "POST",
      url: "/predict",
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Get and display the result
        $(".loader").hide();
        $("#result").fadeIn(600);
        $("#result").text(" Result:  " + data);
        console.log("Success!");
      },
    });
  });
});
