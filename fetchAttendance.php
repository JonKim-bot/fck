<?php
include 'management/getOpenCloseTime.php';

//include 'getOpenCloseTime.php';
function get_total_all_records($parentId){
    $servername = "localhost";
     $username = "u615769276_boitan";
     $password = "password";
     try{
         $connection = new PDO("mysql:host=$servername;dbname=u615769276_finalyear", $username, $password);
     
      }catch(PDOException $e){
         echo "Connection failed: " . $e->getMessage();
     
      }
    $statement = $connection->prepare("SELECT A.*,st.studentId,st.studentName,st.image  FROM Attendance AS A
    INNER JOIN studentTable AS st 
    WHERE st.studentId = A.studentCardId AND st.parentId = '$parentId'");
    $statement->execute();
    return $statement->rowCount();
}

     $servername = "localhost";
     $username = "u615769276_boitan";
     $password = "password";
     try{
         $connection = new PDO("mysql:host=$servername;dbname=u615769276_finalyear", $username, $password);
     
      }catch(PDOException $e){
         echo "Connection failed: " . $e->getMessage();
     
      }//get database connection
   $query = '';
   $output = array(); //user data
   $parentId = $_POST['parentId'];
   
   $query .= "SELECT A.*,st.studentId,st.studentName,st.image FROM Attendance AS A
   INNER JOIN studentTable AS st 
   WHERE st.studentId = A.studentCardId AND st.parentId = '$parentId' ";


if($_POST["is_date_search"] == "yes")
{
  //  echo $_POST["start_date"];
  
    $query .= 'AND A.Datee BETWEEN "'.$_POST["start_date"].'" AND "'.$_POST["end_date"].'" ';

  
}
if(isset($_POST["search"]["value"]) && $_POST["search"]["value"] != "")
{
  //echo $_POST["search"]["value"];
  $query .= 'AND (A.Datee LIKE "%'.$_POST["search"]["value"].'%" ';

  $query .= 'OR st.studentName LIKE "%'.$_POST["search"]["value"].'%" ';
  $query .= 'OR A.Attendance LIKE "%'.$_POST["search"]["value"].'%") ';



 

//  $query .= 'OR studentName LIKE "%'.$_POST["search"]["value"].'%" ';
//  $query .= 'OR pickUpDate LIKE "%'.$_POST["search"]["value"].'%" ';
//append the query one by one
//ELECT * FROM eventTable WHERE EventName LIKE "%bi%" OR EventDate LIKE "%bi%" OR EventMonth LIKE "%bi%" ORDER BY EventId DESC


}

if(isset($_POST["order"]))
{

 $query .= 'ORDER BY '.$_POST['order']['0']['column'].' '.$_POST['order']['0']['dir'].' ';
}
else
{
 $query .= 'ORDER BY Datee DESC ';
}
if($_POST["length"] != -1)

{

 $query .= 'LIMIT ' . $_POST['start'] . ', ' . $_POST['length'];
}

//echo '<script>console.log("'.$query.'")</script>';

  //fetch number of row in filtered row
   //execute the prepare statement 
   // echo "<script>console.log('$query')</script>";
   $statement = $connection ->prepare($query);
   
   $statement->execute();
   //execute the prepare statement 
   $result = $statement->fetchAll();
   //fetch result from prepare statement
   $data = array();
   
   $filtered_row = $statement->rowCount();//fetch number of row in filtered row
 
   
foreach($result as $row){
    // $image = '';
    // if($row['image'] != ""){
    //     $image = '<img src="upload\\'.$row["image"].'" class="img-thumbnail" width="50" height="35" />';
    // }
    // else
    // {
    //  $image = '';
    // }
    // $imageMC = '';
    // if($row['imageMC'] != ""){
    //     $imageMC = '<img src="upload\\'.$row["imageMC"].'" class="img-thumbnail" width="50" height="35" />';
    // }//allow user to upload they mc to here
    // else
    // {
    //  $imageMC = '';
    // }
    $sub_array = array();
    // $sub_array[] = $image;
    $sub_array[] = '<button type="button" name="viewDetail" id="'.$row["AttendanceID"].'" class="btn btn-warning btn-xs viewDetail">View Detail</button>
        ';
    $sub_array[] = $row["studentName"];
    $timeCheckIn = $row['CheckIn'];
    $sub_array[] = $row["Datee"];
    if($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == FALSE && $row['imageMC'] !="" && $row['adminConfirmation'] == "0"){
        $status = '<label class="badge badge-primary">Absent with Mc disapproved</label>';
        
        $sub_array[] = $status;


        $sub_array[] = '<button type="button" name="viewMC" id="'.$row["AttendanceID"].'" class="btn btn-secondary btn-xs viewMC">view MC</button>
        ';


    }elseif($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == FALSE && $row['letter'] !="" && $row['adminConfirmation'] == "1"){
        $status = '<label class="badge badge-primary">Absent with letter provided</label>';
        
        $sub_array[] = $status;


        $sub_array[] = '<button type="button" name="viewLetter" id="'.$row["AttendanceID"].'" class="btn btn-success btn-xs viewLetter">viewLetter</button> ';



    }elseif($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == FALSE && $row['imageMC'] !="" && $row['adminConfirmation'] == "1"){
        $status = '<label class="badge badge-primary">Absent with mc provided</label>';
        
        $sub_array[] = $status;


        $sub_array[] = '<button type="button" name="viewMC" id="'.$row["AttendanceID"].'" class="btn btn-secondary btn-xs viewMC">view MC</button>
        ';


    }elseif($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == FALSE && $row['letter'] !="" && $row['adminConfirmation'] == "0"){
        $status = '<label class="badge badge-primary">Absent with letter disapproved</label>';
        
        $sub_array[] = $status;


        $sub_array[] = '<button type="button" name="viewLetter" id="'.$row["AttendanceID"].'" class="btn btn-success btn-xs viewLetter">viewLetter</button> ';



    }elseif($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == FALSE && $row['imageMC'] !=""){
        $status = '<label class="badge badge-primary">Absent with mc pending approve</label>';
        
        $sub_array[] = $status;


        $sub_array[] = '<button type="button" name="viewMC" id="'.$row["AttendanceID"].'" class="btn btn-secondary btn-xs viewMC">view MC</button>
        ';


    }elseif($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == FALSE && $row['letter'] !=""){
        $status = '<label class="badge badge-primary">Absent with letter pending approve</label>';
        
        $sub_array[] = $status;
       // $sub_array[] = '<button type="button" name="viewLetter" id="'.$row["AttendanceID"].'" class="btn btn-success btn-xs viewLetter">viewLetter</button> ';

       $sub_array[] = '<button type="button" name="viewLetter" id="'.$row["AttendanceID"].'" class="btn btn-success btn-xs viewLetter">viewLetter</button> ';


    }

    elseif($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == TRUE ){
        $status = '<label class="badge badge-primary">Not Yet check in</label>';
        
        $sub_array[] = $status;
        $sub_array[] = 'No need';
    
    }elseif($row['CheckIn'] == "" && $row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == FALSE){
        $status = '<label class="badge badge-primary">absent today</label>';
        
        $sub_array[] = $status;
        $sub_array[] = '<button type="button" name="update" id="'.$row["AttendanceID"].'" class="btn btn-warning btn-sm update">Upload MC</button>
        <div style="margin:20px"></div>
        <button type="button" name="uploadLetter" id="'.$row["AttendanceID"].'" class="btn btn-warning btn-sm uploadLetter">Upload Letter</button>
        ';    


    }else if($row['Checkout'] == "" && getMalaysiaDate() == $row['Datee'] && getCloseTime() == TRUE){
        $status = '<label class="badge badge-primary">Not yet check out</label>';
        $sub_array[] = $status;
        $sub_array[] = 'No need';

        

    }

else{
  
    if($row['CheckIn'] != ""){
        $timeCheckIn = $row['CheckIn'];
        $timeSplit = explode(":",$timeCheckIn);
        $hour = $timeSplit[0];
         $minit = $timeSplit[1];
         $sec = "00";
         $checkInTime = $hour.":".$minit.":".$sec;
        $openTime= getOpenTime($row['Datee']);
        $openTime = $openTime . ":00";
        $timeDiffrence = (strtotime($openTime) - strtotime($checkInTime) )/ 60;
        $status = 0;
        $checkIn = '';
    }else{
        $openTime= getOpenTime($row['Datee']);
        $openTime = $openTime . ":00";
        $checkIn = 'Unavalible';

        $checkInTime = "00:00:00";

    }
    $checkOut = '';
    if($row['Checkout'] != ""){
        $checkOut = $row['Checkout'];
    }else{
        $checkOut = 'Unavalible';
        //if student didn check in and check out , the row will display unablable because they didn come
    }

    
    if(($checkInTime )>($openTime)){

    if($row["Attendance"] == "present")
    {
        $status = '<label class="badge badge-success">Present L'.$timeDiffrence.' min</label>';
        $sub_array[] = $status;

    }

}else{
    if($row["Attendance"] == "present")
			{
                $status = '<label class="badge badge-success">Present</label>                ';
                $sub_array[] = $status;

			}
}
    if($row["Attendance"] == "absent" && $row['imageMC'] != "" && $row['adminConfirmation'] == 1)
    {
        $status = '<label class="badge badge-primary">Absent with mc provided</label>';
        $sub_array[] = $status;

    }else if($row["Attendance"] == "absent" && $row['letter'] != "" && $row['adminConfirmation'] == 1)
    {
        $status = '<label class="badge badge-primary">Absent with letter provided</label>';
        $sub_array[] = $status;

    }
    else if($row["Attendance"] == "absent" && $row['letter'] != "" && $row['adminConfirmation'] == "0")
    {
        $status = '<label class="badge badge-danger">Absent with letter disapproved</label>';
        $sub_array[] = $status;

    }
    else if($row["Attendance"] == "absent" && $row['imageMC'] != "" && $row['adminConfirmation'] == "0")
    {
        $status = '<label class="badge badge-danger">Absent with MC disapproved</label>';
        $sub_array[] = $status;

    }
        else if($row["Attendance"] == "absent" && $row['imageMC'] != "" )
                        {
                            $status = '<label class="badge badge-danger">Absent with mc pending approval</label>
                        
                            ';
                            $sub_array[] = $status;
        
                        }else if($row['Attendance'] == "absent" && $row['letter'] !=""){
                            $status = '<label class="badge badge-danger">Absent with letter pending approval</label>      
        
                            ';
                            $sub_array[] = $status;
        
        
                        }
    else if($row["Attendance"] == "absent" && ($row['letter'] == "" || $row['imageMC'] == "") && ($row['adminConfirmation'] == "" || $row['adminConfirmation'] == 0)){
        $status = '<label class="badge badge-danger">Absent</label>';
        $sub_array[] = $status;


    }else if($row['Attendance'] == "absent"){
        $status = '<label class="badge badge-danger">Absent</label>';
        $sub_array[] = $status;

    }
    
    // $sub_array[] = $imageMC;

    if($row['Attendance'] == "absent" && $row['letter'] == "" && $row['imageMC'] == ""){
    $sub_array[] = '<button type="button" name="update" id="'.$row["AttendanceID"].'" class="btn btn-warning btn-sm update">Upload MC</button>
    <div style="margin:20px"></div>
    <button type="button" name="uploadLetter" id="'.$row["AttendanceID"].'" class="btn btn-warning btn-sm uploadLetter">Upload Letter</button>
    ';
    }else if($row['letter'] !="" && $row['Attendance'] == "absent"){
        $sub_array[] = '<button type="button" name="viewLetter" id="'.$row["AttendanceID"].'" class="btn btn-success btn-xs viewLetter">viewLetter</button>
        ';


    }else if($row['imageMC'] !="" && $row['Attendance'] == "absent"){
        $sub_array[] = '<button type="button" name="viewMC" id="'.$row["AttendanceID"].'" class="btn btn-secondary btn-xs viewMC">view MC</button>
        ';


    }
    else{
        $sub_array[] = 'No need';

    }

    
}
    
    $data[] = $sub_array;
    //fetch data table 
   }
$output = array(
    "draw" =>intval($_POST['draw']),
    "recordsTotal" => $filtered_row,
    "recordsFiltered" => get_total_all_records($parentId),
    "data" => $data
    //C{"draw":3,"recordsTotal":0,"recordFitered = 6 data is all the subarray that appended 

);
echo json_encode($output);
//output the data to main class and append it on datatable

?>