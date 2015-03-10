$(document).ready(function() {
  var allowed_exts = ["mp3"];

  $('#ufile').change(function() { //on file change event   
    var file = $('#ufile').val();
    var ext = file.split(".").pop(); //extract file extension
    if ($.inArray(ext, allowed_exts) == -1) {
      //not allowed extention...
      var error_msg = "file extention not supported";
      alert(error_msg);
      
      
    }
    else {
      var upForm = {
        beforeSend: function() {
          $("#uform_msg").html("");
          $("#bar").width('0%');
          $("#message").html("");
          $("#percent").html("0%");
          $("#analysis_general_msg").html("");
          $("#analysis_attribute_msg").html("");
        },
        uploadProgress: function(event, position, total, percentComplete) {
          $("#bar").width(percentComplete+'%');
          $("#percent").html(percentComplete+'%');
        },
        success: function() {
          $("#bar").width('100%');
          $("#percent").html('100%');
        },
        complete: function(response) {
          response = $.parseJSON(response.responseText);
          console.log(response);
          $.ajax({
            type: "GET",
            url: "http://localhost:8081/things",
            async: false,
            success: function(response)
            {
              console.log(response)
              //response = JSON.parse(response);
             globResp = response;
              for (var i = 0; i < 10; i++) {
                x = getASong(response[i].song, response[i].artist);
                //console.log(x);
                if (x != "error") {
                  console.log(x.preview_url);
                  prevLink[i] = x.preview_url;
                  $("#music_section").append(createSongButton(x.preview_url, x.name, response[i].artist, i));
                };
              };
            },
            error: function() {
              alert("ERROR!!!");
            }
          }); 
        },
        error: function() {
          $("#uform_msg").html("<font color='red'> ERROR: unable to upload files</font>");
          
        }
      }; 
      $("#upload_form").ajaxSubmit(upForm); //submit form


    }
  });
  /*
      $.ajax({
        type: "post",
        url: "explore.php",
        async: false,
        data: {filename: _filename,
               explore: "amp", 
               start: range_min, 
               end: range_max,
               type: filter_type, 
               attrRange: filter_attrRanges,
               fmop: fmop_enum,
               amop: amop_enum,
               pwmop: pwmop_enum,
               blnk: blnk_enum
             },
        success: function(response)
        {

        },
        error: function() {
          alert("ERROR!!!");
        }
      });
*/
});
