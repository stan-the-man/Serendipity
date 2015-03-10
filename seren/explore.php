<?php

  $output_dir = "upload/";
  $return = array();
  //item located in in $_POST['filename'];
  //
  $prog_name = "explore.exe "; //include space after name
  $ext = pathinfo($_POST["filename"]);
  $basename = basename($_POST["filename"], ".".$ext['extension']);

  $attrFilter = $output_dir.$basename."filterRanges.txt";
  $file = fopen($attrFilter, "w");
  fprintf($file, "%d ", $_POST['type']);
  for ($i=0; $i < 8; $i++) { 
    fprintf($file, "%u ", $_POST['attrRange'][$i]);
  } 

  //print MOP enums
  fprintf($file, "%d ", $_POST['fmop']);
  fprintf($file, "%d ", $_POST['amop']);
  fprintf($file, "%d ", $_POST['pwmop']);
  fprintf($file, "%d ", $_POST['blnk']);
  fclose($file);

  $charts = array();

  if ($_POST['explore'] == "freq") {
    $cmd = $prog_name.$output_dir.$_POST['filename']." freq"." ".$_POST['start']." ".$_POST['end']." ".$attrFilter;
    exec($cmd);
    $amp = $output_dir.$basename."-fa_explore.csv";
    $bear = $output_dir.$basename."-fb_explore.csv";
    $pwidth = $output_dir.$basename."-fpw_explore.csv";

    array_push($charts, $amp);
    array_push($charts, $bear);
    array_push($charts, $pwidth);
  }
  if ($_POST['explore'] == "amp") {
    $cmd = $prog_name.$output_dir.$_POST['filename']." amp"." ".$_POST['start']." ".$_POST['end']." ".$attrFilter;
    exec($cmd);
    $freq = $output_dir.$basename."-af_explore.csv";
    $bear = $output_dir.$basename."-ab_explore.csv";
    $pwidth = $output_dir.$basename."-apw_explore.csv";

    array_push($charts, $freq);
    array_push($charts, $bear);
    array_push($charts, $pwidth);
    
  }
  if ($_POST['explore'] == "bear") {
    $cmd = $prog_name.$output_dir.$_POST['filename']." bear"." ".$_POST['start']." ".$_POST['end']." ".$attrFilter;
    exec($cmd);
    $freq = $output_dir.$basename."-bf_explore.csv";
    $amp = $output_dir.$basename."-ba_explore.csv";
    $pwidth = $output_dir.$basename."-bpw_explore.csv";

    array_push($charts, $freq);
    array_push($charts, $amp);
    array_push($charts, $pwidth);
  }
  if ($_POST['explore'] == "pwidth") {
    $cmd = $prog_name.$output_dir.$_POST['filename']." pwidth"." ".$_POST['start']." ".$_POST['end']." ".$attrFilter;
    exec($cmd);
    $freq = $output_dir.$basename."-pwf_explore.csv";
    $amp = $output_dir.$basename."-pwa_explore.csv";
    $bear = $output_dir.$basename."-pwb_explore.csv";

    array_push($charts, $freq);
    array_push($charts, $amp);
    array_push($charts, $bear);
  }

  array_push($return, $charts);
  
  //return array
  /* response payload format:
  // 0 - array of graph filenames  
  */
  echo json_encode($return);

  

?>