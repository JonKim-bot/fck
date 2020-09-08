<!DOCTYPE html>
<?php include("functions.php");?>
<?php include("management/getOpenCloseTime.php");?>

    <html>
        <?php 
        function db()
        {
            //make database conn a gloabal variable
            static $conn;
            if ($conn === NULL)
            {
                $servername = "localhost";
                $username = "u615769276_boitan";
                $password = "password";
                $dbname = "u615769276_finalyear";
                // Create connection
                $conn = new mysqli($servername, $username, $password, $dbname);
            }
            return $conn;
        
        }
//        include('configfb.php');

  session_start(); 
  $kId = $_SESSION['kId'];
  

  if (!isset($_SESSION['parentId'])){
        	header('location: loginParent.php');
  
  }
  if(isset($_SESSION['parentId'])){
    $parentId = getParentId($_SESSION['parentId']);
   
  }
  
  function getParentId($parentEmail){
    $conn = db();
    //get user old password to compare old value and new value , if same then cannot change
    $sql = "SELECT parentId FROM parentTable WHERE email = '$parentEmail'";
    $result = $conn->query($sql);
    if (!$result)
    {
        trigger_error('Invalid query: ' . $conn->error);
    }
    if ($result->num_rows > 0)
    {
        while ($row = $result->fetch_assoc())
        {
            return $row['parentId'];
            //password is correct
            
        }

    }

  }
  if (isset($_GET['logout'])) {
  	session_destroy();
  	  	unset($_SESSION['parentId']);
  	  	  	  	unset($_SESSION['userType']);


  	header("location: loginParent.php");
  }
 
  function getGradeName($grade_id){
       
    $conn = db();
    
    $sql = "SELECT grade_name FROM tblGrade WHERE grade_id='$grade_id'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0 ) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            return $row['grade_name'];
        }
    }else{
        return "none";
    }
     }

  function getStudentName($studentId){
       
    $conn = db();
    
    $sql = "SELECT studentName FROM studentTable WHERE studentId='$studentId'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0 ) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            return $row['studentName'];
        }
    }else{
        return "none";
    }
     }
function getNotificationMsg($parentName,$studentName,$checkInOutTime,$date,$customMessage){
   
        return "".$studentName. " ".$customMessage. " at ".$checkInOutTime;

    
}
?>

<head>
    <meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <title>Parent Monitor APP</title>
<meta name="description" content="Our company had come out a very innovative and creative product which is a very powerful and functionality pick-up system to protect the student!">
<meta name="keywords" content="rfid parent login,">
<meta name="robots" content="index, follow">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="language" content="English">
<meta name="revisit-after" content="1 days">
<meta name="author" content="Boitan">    
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:400,400i,700,700i,600,600i">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/simple-line-icons/2.4.1/css/simple-line-icons.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/baguettebox.js/1.10.0/baguetteBox.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/limonte-sweetalert2/8.11.8/sweetalert2.all.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/limonte-sweetalert2/8.11.8/sweetalert2.js"></script>
    <!-- Optional: include a polyfill for ES6 Promises for IE11 -->
    <script src="https://cdn.jsdelivr.net/npm/promise-polyfill"></script>
    <script
    src="https://code.jquery.com/jquery-3.4.1.js"
    integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU="
    crossorigin="anonymous"></script>
    <script type="text/javascript" src="js/jquery.js"></script>
    <script type="text/javascript" src="js/qrcode.js"></script>
    <link rel="stylesheet" href="css/style.css">
    <link rel="shortcut icon" href="https://i.pinimg.com/originals/d0/53/f2/d053f2394d420d8d3712046f4e8f80cc.jpg" />

    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/js/all.min.js" crossorigin="anonymous"></script>


    <link href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css" rel="stylesheet" crossorigin="anonymous" />
        
    <script src="https://apis.google.com/js/client:platform.js?onload=onLoad" async defer></script> 

<meta name="google-signin-client_id" content="711631038582-5din927pouhjmfiakr6so65fshcc8vtp.apps.googleusercontent.com">

  <style>
  @-webkit-keyframes blinker {
  from {opacity: 1.0;
    background: red;
  }
  to {opacity: 0.0;}
}
.blink{
	text-decoration: blink;
	-webkit-animation-name: blinker;
	-webkit-animation-duration: 0.6s;
	-webkit-animation-iteration-count:infinite;
	-webkit-animation-timing-function:ease-in-out;
	-webkit-animation-direction: alternate;
}
.fixedSideNav {
  max-height: 100%;
  position: fixed;
  overflow-y: scroll;
}
@media only screen and (max-width: 990px) {
  #topDiv {
    
      margin:0px;
  }
   #topDiv2{
    display:none;
      margin:0px;
  }
 
}

      .qrcode-container {
    text-align: center;
    width: 128px;
    height: 128px;
    margin:  0 auto;
 }
 .dropdown-menu {
  min-width:inherit;
}        .dropdown-menu{
   max-height:250px;/* you can change as you need it */
   overflow:auto;/* to get scroll */
}
  </style>
  <script>
  parentId = "<?php 
    echo $parentId;
  ?>";
  $.ajax({
      //get tidio chat user details
      url:"tidioDetail.php",
      method:"POST",
      data:{getParentDetail : "1",parentId : parentId},
      dataType:"json",
     
      success:function(data)
	
      {
	console.log(parentId);
	console.log(data);
	//return json value
	
        if(data.success)
        {
            console.log("sucess");
         document.tidioIdentify = {
  distinct_id: "<?php echo $parentId?>", // Unique user ID in your system
  email: data.parentEmail, // User email
  name: data.parentName, // Visitor name
  country: "MY", // Country
  phone:"+60 "+ data.phoneNumber
};
(function() {
  function onTidioChatApiReady() {
    //window.tidioChatApi.open();
    // for(var i=0;i<10;i++){
//window.tidioChatApi.messageFromVisitor("Hi!My Name is" + data.parentName);
//}
  }
  if (window.tidioChatApi) {
         window.tidioChatApi.on("ready", onTidioChatApiReady);

  } else {
    document.addEventListener("tidioChat-ready", onTidioChatApiReady);
   
  }
})();

            
        }else{
            console.log("fail");
        }
      }
  });
    

    function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
                auth2.disconnect();
    console.log("no connect");;
    
}
function onLoad() {
      gapi.load('auth2', function() {
        gapi.auth2.init();
        console.log("inited");
      });
    }//seperate page have to put this to load auth
 


   



  </script>

</head>

<body>

    <nav class="navbar navbar-light navbar-expand-lg fixed-top bg-white clean-navbar fixedSideNav">
        <div class="container"><a class="navbar-brand " href="qrpage1.php">Parent Monitor</a>
        <?php
            $todayDate = getMalaysiaDate();
            $yesterday = date("Y-m-d", time()-86400);
            $query = "SELECT * from `tblNotifications` where `status` = 'unread' and `parentId` = '$parentId' and (`msgDate` = '$todayDate' or `msgDate` = '$yesterday')  order by `msgDate`,`checkInOutTime` DESC";
            $query2 = "SELECT `subcribeStatus`  from `parentTable` WHERE `parentId` = '$parentId' AND `subcribeStatus` IS NULL";

            if(count(fetchAll($query))>0 || count(fetchAll($query2))>0){
            ?>
        <button data-toggle="collapse" class="navbar-toggler blink" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span>
        </button>
        <?php
                            }else{

                          
                                ?>
                                 <button data-toggle="collapse" class="navbar-toggler" data-target="#navcol-1"><span class="sr-only">Toggle navigation</span><span class="navbar-toggler-icon"></span>
        </button>
        <?php 
        }?>
    
            <div class="collapse navbar-collapse"
                id="navcol-1" >
                <ul class="nav navbar-nav ml-auto">
                   
                    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" style="font-size: 1.0rem;" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Booking
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
          <a class="dropdown-item" href="qrpage1.php">Qr Code Generate</a>
                    <a class="dropdown-item" href="qrpage2.php">Read Qr Code</a>

          <a class="dropdown-item" href="qrparent.php">Check My Booking</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" style="font-size: 1.0rem;" href="#" id="navbarDropdownMenuLink2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Details
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink2">
          <a class="dropdown-item"  href="parentDetail.php">Parent Detail</a>
                    <a class="dropdown-item" href="updateChildrenDetail.php">Children Details</a>

          <a class="dropdown-item" href="studentAttendance.php">Children Attendance</a>
          <a class="dropdown-item"href="viewAllTeacher.php">View All Teachers</a>
                    <a class="dropdown-item" href="changePasswordParent.php">Change Password</a>

        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" style="font-size: 1.0rem;" href="#" id="navbarDropdownMenuLink3" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Others
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink3">
          <a class="dropdown-item" href="vParentNotification.php">Notification History</a>
                              <a class="dropdown-item" href="provideFeedBack.php">FeedBack</a>
                    <a class="dropdown-item" href="viewPostForParent.php">Site News</a>

                    <a class="dropdown-item"  href="userGuideGps.php">GPS Guide</a>

        
        </div>
      </li>
               
                    <li class="nav-item dropdown" >
                        <a class="nav-link" style="font-size:1rem" href="http://example.com" id="dropdown01" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Notifications 
                          <!-- parent  name-->
                          
                         <?php if(count(fetchAll($query))>0){
                 ?>
                            <span class="badge badge-dark blink"><?php echo count(fetchAll($query)); ?></span>
                          <?php
                         
                         }
                         
                                ?>
                          </a>
                          
                        <div class="dropdown-menu" aria-labelledby="dropdown01">
                            <?php
                         
                         
                            $query = "SELECT * from `tblNotifications` where `parentId` = '$parentId' and (`msgDate` = '$todayDate' or `msgDate` = '$yesterday') order by `msgDate` DESC";
                             if(count(fetchAll($query))>0){
                                 foreach(fetchAll($query) as $i){
                                     //fetch all function , niubi
                                     //pass query parameter to there

                            ?>
                          <a style ="
                                     <?php
                                        if($i['status']=='unread'){
                                            echo "font-weight:bold;";
                                        }
                                     ?>
                                     " class="dropdown-item" href="view.php?notificationId=<?php echo $i['notificationId'] ?>">
                            <small><i><?php echo ($i['msgDate']) ?></i></small><br/>
                              <?php 
                              
                              $parentName = $i['parentName'];
                              $studentName = getStudentName($i['studentId']);
                              $checkInOutTime = $i['checkInOutTime'];
                              $date = $i['msgDate'];
                              
                            if($i['type']=='CheckIn'){
                               echo getNotificationMsg($parentName,$studentName,$checkInOutTime,$date,"checked in");

                            }else if($i['type']=='CheckOut'){
                                echo getNotificationMsg($parentName,$studentName,$checkInOutTime,$date,"checked out");
                            } else if($i['type']=='pickUp'){
                                echo getNotificationMsg($parentName,$studentName,$checkInOutTime,$date," got picked up");
                            }
                             else if($i['type']=='qrPickUp'){
                                echo getNotificationMsg($parentName,$studentName,$checkInOutTime,$date," got picked up");
                            }
                              
                              
                              ?>
                            </a>
                          <div class="dropdown-divider"></div>
                            <?php
                                 }
                             }else{
                                 echo "<p>No Records yet. <p>";
                             }
            
                                 ?>
                        </div>
                      </li>  
                        <?php if(count(fetchAll($query2))>0){?>
                                  <li class="nav-item" role="presentation" style="font-size: 1.2rem;"><a class="nav-link" style="font-size:1rem;" href="subcribeNotification.php">Subcribe Notification
                                  
                                  <span class="badge badge-dark blink"><?php echo count(fetchAll($query2)); ?></span>

                                  </a></li>
                                  <?php }else{?>
                                    <li class="nav-item" role="presentation" style="font-size: 1.2rem;"><a class="nav-link" style="font-size:1rem;" href="subcribeNotification.php">Subcribe Notification

                                    
                                    </a></li>
                                    <?php }?>
                      
                      
                           
                         <li class="nav-item" role="presentation" style="font-size: 1.2rem;"><a class="nav-link" style="font-size:1rem;" href="qrpage1.php?logout='1'" onclick="signOut()">Log Out</a></li>
                            </li>
                        
                </ul>
            </div>
        </div>
        
    </nav>
    <div id="topDiv2" style="margin:150px"></div>