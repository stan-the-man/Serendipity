$(document).ready(function() {
  //var fileURL = [{"artist": "Casual", "song": "I Didn't Mean To"}, {"artist": "The Box Tops", "song": "Soul Deep"}, {"artist": "Sonora Santanera", "song": "Amor De Cabaret"}, {"artist": "Adam Ant", "song": "Something Girls"}, {"artist": "Gob", "song": "Face the Ashes"}, {"artist": "Jeff And Sheri Easter", "song": "The Moon And I (Ordinary Day Album Version)"}, {"artist": "Rated R", "song": "Keepin It Real (Skit)"}, {"artist": "Planet P Project", "song": "Pink World"}, {"artist": "Clp", "song": "Insatiable (Instrumental Version)"}, {"artist": "JennyAnyKind", "song": "Young Boy Blues"}];
  //thing = JSON.parse(fileURL);
  //console.log(thing);

  /* DEFAULT CONFIG & GLOBAL VAR'S

  */
  //asdf = ["https://p.scdn.co/mp3-preview/2ef31d23f9d52a18c24a1358f590c18b5e11db77"];
  $("#textSearch").hide();

  /*

  $("#music_section").append(createSongButton(asdf,"SOC NIGGA", 1));
  $("#song1").click(function() {
    var mySound = soundManager.createSound({
      url: asdf[0]
    });
    mySound.play();
  })
*/
musicShit = [];
getURL = "https://api.spotify.com/v1/tracks/";
trackID = "4LujRMTMwAfFKjm45tixHY";
lastUsed = null;
mySound = [];
prevLink = [];
globResp = null;

/* KEEP OUT FOR DEMOOOO
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
*/
/*
$.ajax({
  type: "post",
  url: "http://localhost:8081/things/nigga",
  //data: "{'filename':'asdf'}",
  async: false,
  success: function(response)
  {
    console.log(response)
    
  },
  error: function() {
    alert("ERROR!!!");
  }
});
*/
//console.log(getSongData(trackID));
/*
  x = searchData();
  x = x.tracks.items;
  //console.log(x);
  mySound = [];
  
  var songName = [];
  prevLink = [];
  for (var i = 0; i < x.length; i++) {
    songName[i] = x[i].name;
    prevLink[i] = x[i].preview_url;
    $("#music_section").append(createSongButton(prevLink[i], songName[i], i));
     
      
  };
  */
   //niggersssss = getASong("levels", "Avicii");
   //console.log(niggersssss);

   //getSimSongs("i didn't mean to",  "casual");
});

function getSimSongs (num) {
  if (lastUsed != null) {
  soundManager.destroySound("s"+String(lastUsed));
  //lastUsed = i;
 };
  artName = globResp[num].artist;
  songName = globResp[num].song;
  searchDIS = "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist="+artName+"&track="+songName+"&api_key=681a034989f7507820af5caa8b6ff1a0&format=json"
  $.ajax({
    type: "post",
    url: searchDIS,
    async: false,
    success: function(response)
    {
      console.log(response.similartracks)
      globResp[0].artist = response.similartracks['@attr'].artist;
      globResp[0].song = response.similartracks['@attr'].track;
      x = getASong(globResp[0].song, globResp[0].artist);
      prevLink[0] = x.preview_url;
      $("#music_section").html(createSongButton(x.preview_url, x.name, globResp[0].artist, 0));

      for (var i = 1; i < 10; i++) {
        globResp[i].artist = response.similartracks.track[i].artist.name;
        globResp[i].song = response.similartracks.track[i].name;
      };
      
      for (var i = 1; i < 10; i++) {
        x = getASong(globResp[i].song, globResp[i].artist);
        //console.log(x);
        if (x != "error") {
          //console.log(response[i].artist);
          prevLink[i] = x.preview_url;
          $("#music_section").append(createSongButton(x.preview_url, x.name, globResp[i].artist, i));
        };

      };
    
    },
    error: function() {
      alert("ERROR!!!");
    }
  });
}


function getsomething() {
  var serverURL = "http://localhost:7474/db/data"
  $.ajax({
    type:"POST",
    url: serverURL + "/cypher",
    accepts: "application/json",
    dataType: "json",
    contentType:"application/json",
    headers: { 
      "X-Stream": "true"    
    },
    data: JSON.stringify({
       "query" : "MATCH (n) RETURN n LIMIT 10",
       "params" : {}
     }),
    success: function(response)
    {
      
      console.log(response.data[0])
       //alert(JSON.stringify(data, null, 4));
      //retData = response;
    },
    error: function(jqXHR, textStatus, errorThrown){
     alert(errorThrown);
     console.log(textStatus);
    }
  });//end of ajax
  } //end of getSomething()


function playSoundPrev (i) {
  //console.log(prevLink)
 //mySound[lastUsed].mute();
 //soundManager.mute("s"+String(lastUsed));
 //console.log(lastUsed);
 if (lastUsed != null) {
  soundManager.destroySound("s"+String(lastUsed));
  //lastUsed = i;
 };
 
  //soundManager.unmute("s"+String(lastUsed));
  mySound[i] = soundManager.createSound({
    id: "s"+ String(i),
    url: prevLink[i],
    whileplaying: function() {
      //console.log(position)
      //soundManager._writeDebug('sound '+this.id+' playing, '+this.position+' of '+this.duration);

    }

  });
  //mySound[i].play();
  lastUsed = i;
  soundManager.play("s"+String(i));
}

function stopSound (i) {
  //console.log(prevLink)
 //mySound[lastUsed].mute();
 //soundManager.mute("s"+String(lastUsed));
 //console.log(lastUsed);
 if (lastUsed != null) {
  soundManager.destroySound("s"+String(lastUsed));
  lastUsed = null;
 } else {
  console.log("wtfnigga");
 };

}


function createSongButton (url, name, art, number) {
  globResp[number].song = name;
  globResp[number].artist = art;

  DisplayText = '<div id="song'+number+'" class="btn btn-default btn-lg dispText">'+name+" - "+art+'</div>';
  string1 = '<button id="song'+number+'" type="button" onclick="playSoundPrev('+number+')" class="play-btn btn btn-default btn-lg"><span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>';
  string2 = '<button type="button" onclick="getSimSongs('+number+')" class="play-btn btn btn-default btn-lg"><span class="glyphicon glyphicon-search" aria-hidden="true"></span></button>';
  string3 = '<button type="button" onclick="" class="play-btn btn btn-default btn-lg"><span class="glyphicon glyphicon-heart" aria-hidden="true"></span></button></br></br>';
  string4 = '<button type="button" onclick="stopSound('+number+')" class="play-btn btn btn-default btn-lg"><span class="glyphicon glyphicon-stop" aria-hidden="true"></span></button>';

   return DisplayText+string1+string4+string2+string3;
}

function getSongData (trackID) {
  getURL = "https://api.spotify.com/v1/tracks/";
  var retData;
  $.ajax({
    type: "get",
    url: getURL+trackID,
    async: false,
    success: function(response)
    {
      //console.log(response)
      retData = response;
    },
    error: function() {
      alert("ERROR!!!");
    }
  });
  return retData;

}

function searchData (rand_param) {
  getURL = "https://api.spotify.com/v1/search?q=i&type=track&limit=10";
  var retData;
  $.ajax({
    type: "get",
    url: getURL,
    async: false,
    success: function(response)
    {
      //console.log(response)
      retData = response;
    },
    error: function() {
      alert("ERROR!!!");
    }
  });
  return retData;

}

function getSongList (_songList) {
  var retData = [];
  for (var i = 0; i < _songList.length; i++) {
    retdata[i] = getASong(_songList[i].song, _songList[i].artist);
  };
  return retData;
}

function getASong (_sname, _artist) {
  getURL = "https://api.spotify.com/v1/search?q="+_sname+"&type=track&limit=25";
  var retData = null;
  $.ajax({
    type: "get",
    url: getURL,
    async: false,
    success: function(response)
    {
      //console.log(response)
      Data = response.tracks.items;
      //console.log(Data[0].artists[0].name)
      for (var i = 0; i < Data.length; i++) {
        //art = Data[i].artists;
        if (Data[i].artists[0].name == _artist) {
          retData = Data[i];
          break;
        };
      };
    },
    error: function() {
      alert("ERROR!!!");
    }
  });
  if (retData != null) {
    return retData;
  } else {
    //console.log("Error in getAsong()");
    retData = "error";
    return retData;
  };
  
}

function dispFileSection () {
  
    $("#textSearch").hide();
    $("#fileSearch").show();



}

function dispTextSection () {
 
    $("#fileSearch").hide();
    $("#textSearch").show();
}