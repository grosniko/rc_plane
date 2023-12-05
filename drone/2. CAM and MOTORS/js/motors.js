var pct = 90
var mvmt = "roll"

function move_servo(e){

    power_levels = {
          "off":0,
          "low": parseInt(document.getElementById("low_val").value),
          "mid": parseInt(document.getElementById("mid_val").value),
          "high": parseInt(document.getElementById("high_val").value)
      }

	pct = e.value
	mvmt = e.id
	var pwr_indicator = displayPwrValue()
    var pwr = power_levels[pwr_indicator]
	var param_str = "input="+mvmt+"-"+pct+"-"+pwr
	callPHP(param_str)
}

function motor_power(){

    power_levels = {
          "off":0,
          "low": parseInt(document.getElementById("low_val").value),
          "mid": parseInt(document.getElementById("mid_val").value),
          "high": parseInt(document.getElementById("high_val").value)
      }

    var pwr_indicator = displayPwrValue()
    var pwr = power_levels[pwr_indicator]
    var param_str = "input="+mvmt+"-"+pct+"-"+pwr
    callPHP(param_str)
}

function addToUI(text){
    var arrows = document.getElementById("arrows")
    var camera = document.getElementById("ctrl_type")
    var faster = document.getElementById("faster")
    var annotation = "%Y.%M.%D_%h:%m:%s"
    if(arrows.checked){
        annotation += " -A "
    }
    if(camera.checked){
        annotation += "-C "
    }
    if(faster.checked){
        annotation += "-F "
    }

    annotation += text
    annotation += cur_pos()
    send_cmd('an ' + encodeURI(annotation))
    
}
 


function control(e){
  if(document.getElementById("arrows").checked){
      if(e.keyCode === 65){document.getElementById("arrows").checked = false}
      e.preventDefault();
      e = e || window.event;
      var type_cb = document.getElementById("ctrl_type")
      var faster = document.getElementById("faster")
      if(type_cb.checked == false){
            var roll = document.getElementById("roll")
            var yaw = document.getElementById("yaw")
            var roll_type = "roll"
            var yaw_type = "yaw"
        } else {
            var roll = document.getElementById("cam_x")
            var yaw = document.getElementById("cam_y")
            var roll_type = "cam_x"
            var yaw_type = "cam_y"
        }
      var increment = 1
      if(faster.checked){
        increment += 9
      }
        // console.log("pressed", e.keyCode)
      if (e.keyCode === 38) {
                yaw.value = parseInt(yaw.value) + increment
                move_servo({"value": yaw.value, "id": yaw_type})
      } else if (e.keyCode === 40) {
                yaw.value -= increment
                move_servo({"value": yaw.value, "id": yaw_type})    
      } else if (e.keyCode === 37) {
                roll.value -= increment
                move_servo({"value": roll.value, "id": roll_type})    
      } else if (e.keyCode === 39) {
                roll.value = parseInt(roll.value) + increment
                move_servo({"value": roll.value, "id": roll_type})
      } else if(e.keyCode === 67){
        
        if(type_cb.checked){
            type_cb.checked = false
        } else {
            type_cb.checked = true
        }
        addToUI("")
      } else if(e.keyCode === 86){
        
        if(faster.checked){
            faster.checked = false
        } else {
            faster.checked = true
        }
        addToUI("")
      }
  } else if(e.keyCode === 65){
    document.getElementById("arrows").checked = true
  }
}

var current_pos = {
    "roll": "roll-90",
    "yaw": "yaw-90",
    "cam_x": "cam_x-90",
    "cam_y": "cam_y-90"
}

function cur_pos(){
    var str = current_pos["roll"] + " " + current_pos["yaw"] + " " + current_pos["cam_x"] + " " + current_pos["cam_y"]
    return str
}

function callPHP(params) {
    var httpc = new XMLHttpRequest(); // simplified for clarity
    var url = "pca.php";
    httpc.open("POST", url, true); // sending as POST
    httpc.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    httpc.onreadystatechange = function() { //Call a function when the state changes.
        if(httpc.readyState == 4 && httpc.status == 200) { // complete and no errors
            console.log(httpc.responseText); // some processing here, or whatever you want to do with the response
            if(httpc.responseText.includes("on")){
            	alert("Connecting to controls. Try again in 3 seconds...")
            } else
            if(httpc.responseText.includes("Python ERROR!")){
                alert("Couldn't launch controls. Check the python!")
            } else {
                var a = httpc.responseText
                if(a.includes("roll")){
                    current_pos["roll"] = a
                }
                if(a.includes("yaw")){
                    current_pos["yaw"] = a
                }
                if(a.includes("cam_x")){
                    current_pos["cam_x"] = a
                }
                if(a.includes("cam_y")){
                    current_pos["cam_y"] = a
                }
                addToUI("")
            }
            
        }
    };
    httpc.send(params);
}


function displayPwrValue() {
            var ele = document.getElementsByName('drone');
 
            for (i = 0; i < ele.length; i++) {
                if (ele[i].checked)
                    return ele[i].value
            }
        }