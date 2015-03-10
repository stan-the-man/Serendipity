<?php

  $output_dir = "upload/";
  $return = array();
  
  
  if ($_FILES["myfile"]["error"] > 0) {
    array_push($return, "err1"); //error uploading file
  } else  {
      $old_files = glob($output_dir."*"); // get all file names
      foreach($old_files as $ofile){ // iterate files
        if(is_file($ofile))
          unlink($ofile); // delete file
      }
      //move temp file into designated upload directory
      move_uploaded_file($_FILES["myfile"]["tmp_name"],$output_dir. $_FILES["myfile"]["name"]);
      //$progarm = "python getBeats.py ".$output_dir. $_FILES["myfile"]["name"]." &";
      //exec($progarm);
      //sleep(10);
     array_push($return, $output_dir. $_FILES["myfile"]["name"]);
  }
  echo json_encode($return);
?>