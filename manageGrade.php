<?php require 'topNav.php';?>


</script>
<?php if (isset($_SESSION['teacherId'])){
    echo "<script>location.href='manageStudent.php'</script>";
}
?>
<style>
    .bg-darker{
        background:#282828;
    }
</style>
                <main>
                    <div class="container-fluid bg-darker" >
                    <div class="card mb-4 bg-darker" style="clear:both;border:20">
                       <hr style="background:white">
                        <div class="card-header text-center"><h1 class="text-center text-white">Grade Details</h1> 
                         <p>Below are all the details of the registered grade, it is use to keep track of the student in the different grade.
                         Note: after you click the delete button , you have to assign new grade to all student and teacher which their grade became null.
                         </p>
                        </div>
                        <hr style="background:white">
                        <button type="button" id="add_button" class="btn btn-info btn-lg" style="width:50%;margin:auto;">Register New Grade</button>

                            <div class="card-body" style="border-radius:3%">
                                
                                <div class="table-responsive bg-black" style="border-radius:1%;padding:10px">
                                   

                                    <table class="table table-bordered table-dark table-striped table-hover" id="dataTable" width="100%" cellspacing="0">
                                        <thead>
                                            <tr>
                                            
                                               
                                            <th>Grade Name</th>
                                             
                                             <th>View</th>
 
                                             <th>Update</th>
                                             <th>Delete</th>
 
                                            </tr>
                                        </thead>
                                        
                                     

                                    
                                      


                                        <tfoot>
                                            <tr>
                                             
                                            <th>Grade Name</th>
                                             
                                            <th>View</th>

                                            <th>Update</th>
                                            <th>Delete</th>




                                            </tr>
                                        </tfoot>
                                        
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
                <footer class="py-4 bg-dark mt-auto">
                    <div class="container-fluid bg-dark">
                        <div class="d-flex align-items-center justify-content-between small bg-dark">
                            <div class="text-muted">Copyright &copy; Tian <?php echo date("Y");?></div>
                            <div>
                                <a href="#">Privacy Policy</a>
                                &middot;
                                <a href="#">Terms &amp; Conditions</a>
                            </div>
                        </div>
                    </div>
                </footer>
            </div>
        </div>
        <div class="modal fade" id="viewModal"  >
  <div class="modal-dialog modal-lg" style="background:#282828;border-radius:3%">
    <div class="modal-content">

      <!-- Modal Header -->
      <div class="modal-header">
        <h4 class="modal-title">Grade Details</h4>
        <button type="button" class="close" data-dismiss="modal">&times;</button>
      </div>

      <!-- Modal body -->
      <div class="modal-body" style="background:#282828;border-radius:1%" id="grade_details">
      </div>

      <!-- Modal footer -->
      <div class="modal-footer">
      <button type="button" name="create_report_teacher" id="create_report_teacher" class="btn btn-success btn-sm">Create Teacher Report</button>

      <button type="button" name="create_report" id="create_report" class="btn btn-primary btn-sm">Create Student Report</button>

        <button type="button" class="btn btn-danger btn-sm" data-dismiss="modal">Close</button>
      </div>

    </div>
  </div>
</div>

          <script>

     window.addEventListener("load",function(){
                        getSelectedValue(document.getElementById('kId').options[document.getElementById('kId').selectedIndex].value);
                    

                        //onload to load the textbox data
                    },false);
                    </script>
<div id="eventModal" class="modal fade">
 <div class="modal-dialog bg-dark" >
  <form method="post" id="grade_form" enctype="multipart/form-data">
   <div class="modal-content bg-dark">
    <div class="modal-header text-white">
     <h4 class="modal-title">Add Grade</h4>
     <button type="button" class="close" data-dismiss="modal">&times;</button>

    </div>
    <div class="modal-body bg-dark" id="grade_details">
   
    <div class="modal-body text-white">
        <div id="gradeDiv">
        <label><b>Kindergarden ID :</b></label>

                            <?php
                               function db () {
    //make database conn a gloabal variable
   static $conn;
   if ($conn===NULL){ 
     $servername = "localhost";
       $username = "u615769276_boitan";

       $password = "password";
       $dbname = "u615769276_finalyear";
       // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);    
           }
   return $conn;
}//get database connection

                           // $parentId = "867364651663";
                           $kId = $kindergardenId;
                           
                            // Create connection
                            $conn = db();
                            if($kId == 0){
                                echo '<select class="form-control" name = "kId" id="kId" onChange="getSelectedValue(this.options[this.selectedIndex].value)">';

                                                            $sql = "SELECT kId FROM tblKindergarden";

                            }else{
                                echo '<select class="form-control" disabled name = "kId" id="kId" onChange="getSelectedValue(this.options[this.selectedIndex].value)">';

                                                            $sql = "SELECT kId FROM tblKindergarden WHERE kId = '$kId'";

                            }
                            //later change this to student name
                            $result = $conn->query($sql);
                            if ($result->num_rows > 0 ) {
                                // output data of each row
                                while($row = $result->fetch_assoc()) {
                                    if (!empty($row['kId'])) {
                                       
                                                echo "<option id='myoption'>".$row['kId']."</option>";
                                            

                                      // echo "<option>".$row['studentId']."</option>";
                                        //use drop down to get the value of children
                                        
                                    }else{
                                        echo "<option>Not found</option>";

                                    }
                                }
                            }                        
                        
                               // echo json_encode($obj);
                        
                                    
                                
                            
                                
                             else{
                                echo "<option>No New Parent found,please go to the machine and register".$kId."</option>";

                            }
                            ?>
                                    </select>

                                 <br />  
                                 
                                         </div>
                                          <label><b>Kindergarten Name :</b></label>
     <input type="text" name="kName" id="kName" disabled class="form-control"/>
     <br />  
          

     <label><b>Grade Name :</b></label>
     <input type="text" name="gradeName" id="gradeName" class="form-control" pattern=".{3,15}" title="Please re-enter your grade name , At least 3 characters and maximum 15 characters" required placeholder="Enter the grade name here"/>
     <br />  
          

    </div>
    <div class="modal-footer">
     <input type="hidden"  name="user_id" id="user_id" />
          <input type="hidden"  name="kIdH" id="kIdH" />

     <input type="hidden" name="operation" id="operation" />

     <input type="submit" name="action" id="action" class="btn btn-success" value="Add" />
     <button type="button" class="btn btn-danger" id="closeForm" data-dismiss="modal">Close</button>
    </div>
   </div>
  </form>
 </div>
</div>




 <script>

     function getSelectedValue(chosen) {
 // console.log(chosen);
 console.log(chosen);
 getKName(chosen);
//chosen is the id of student

}

function getKName(kId) {
    //onchange then call ajax function
    $.ajax({
        type: "post",
        url: "getPNSdetail.php",
        data: {getKName : "1",kId : kId},
        success: function(data) {
            document.getElementById("kName").value = data;
        }
    });
}
</script>


<?php require 'footerAdmin.php';?>
<script type="text/javascript" language = "javascript">
// The ready() method is used to make a function available after the document is loaded. Whatever code you write inside the $(document ).ready() method will run once the page DOM is ready to execute JavaScript code.
$(document).ready(function(){
    function enableBtn(text){
            $('#action').val(text);
            $('#action').attr('disabled', false);
            $('.viewGrade').text("View");
            $('.viewGrade').attr('disabled', false);
            $('.update').text("Update");
            $('.update').attr('disabled', false);
          }
   
 var dataTable = $('#dataTable').DataTable({
  "processing":true,
  "serverSide":true,
  "order":[],
  "ajax":{
   url:"fetch_all.php",
   type:"POST",
    'data': {
        fetchGrade : "1",
        // post data to ajax qr page
        },
  "columnDefs":[
   {
    "targets":[0],
    "orderable":false,
   },
  ],

 }
});
$(document).ready(function(){
    $(document).on('click', '.viewGrade', function(){
    user_id = $(this).attr('id');
    console.log(user_id);
    $.ajax({
      url:"fetch_single_all.php",
      method:"POST",
      data:{action:'fetchGradeStudent', user_id:user_id},
      beforeSend:function(){
            $('.viewGrade').text('Processing...');
            $('.viewGrade').attr('disabled', 'disabled');
          },
      success:function(data)
      {
          enableBtn("Edit");
        $('#viewModal').modal('show');
        $('.modal-title').text("View Grade Detail");

        $('#grade_details').html(data);

      }
    });
        });


        $('#create_report_teacher').click(function(){
            var user_id = $('#td_grade_id').text();
            var numOfTeacherGrade = $('#numOfTeacherGrade').text();
            console.log(numOfTeacherGrade);

            console.log(user_id);
            if(numOfTeacherGrade != 0 ){
             window.open("report.php?action=generateGradeReportTeacher&grade_id="+user_id);
            }else{
                Swal.fire({
        title: 'No Teacher in this grade',
        text: "Empty Teacher are not allowed!",
        type: 'error'
        })
            }

  });

  $('#create_report').click(function(){
            var user_id = $('#td_grade_id').text();
            var numOfStudentGrade = $('#numOfStudentGrade').text();
            console.log(numOfStudentGrade);

            console.log(user_id);
            if(numOfStudentGrade != 0 ){
             window.open("report.php?action=generateGradeReport&grade_id="+user_id);
            }else{
                Swal.fire({
        title: 'No student in this grade',
        text: "Empty student are not allowed!",
        type: 'error'
        })
            }

  });



 //parent Pop Up Form
 $(document).on('submit', '#grade_form', function(event){
  event.preventDefault();//this method will stop summit form data
  var gradeName = $('#gradeName').val();
    var kId = $('#kId').val();

  var action = $('#action').val();
console.log("submit grade form");
  if(gradeName != '')
  {
    var queryString = $('#grade_form').serialize();
//alert(queryString);
   $.ajax({
    
    url:"insert_all_edit.php",
    method:'POST',
    data:new FormData(this),
    contentType:false,
    processData:false,
    beforeSend:function(){
            $('#action').val('Processing...');
            $('#action').attr('disabled', 'disabled');
          },
    success:function(data) //call this function after success
    {
    // alert(data);
     if(data =="grade name existed" && action == "Edit"){
                                             $('#gradeName').focus()

        Swal.fire({
        title: 'Grade name existed',
        text: "Same grade name are not allowed!",
        type: 'error'
        })
        enableBtn("Edit");
      
     }else if(data =="grade name existed" && action == "Register"){
                                                      $('#gradeName').focus()

        Swal.fire({
        title: 'Grade name existed',
        text: "Same grade name are not allowed!",
        type: 'error'
        })
        enableBtn("Register");
      
     }else if(action == "Edit"){
        Swal.fire({
        title: 'Updated Success',
        text: "Grade updated!",
        type: 'success'
        })
        $('#grade_form')[0].reset();
        enableBtn("Edit");

$('#eventModal').modal('hide');
//hide the table after success
dataTable.ajax.reload();
     }else if(action == "Register"){
        Swal.fire({
        title: 'Registered Success',
        text: "New grade added!",
        type: 'success'
        })
        enableBtn("Register");

        $('#grade_form')[0].reset();

$('#eventModal').modal('hide');
//hide the table after success
dataTable.ajax.reload();
     }else{
         alert("none");
     }
    }
   });
  }
  else
  {
    Swal.fire({
        title: 'Please Enter All Details',
        text: "Empty field are not allowed!",
        type: 'warning'
        })
  }
 });



 $('#add_button').click(function(){
    $('#eventModal').modal('show');   
            $('#kId').attr('disabled', false);

    $('#action').val("Register");
    $('#operation').val("insertGrade");
    $('.modal-title').text("Register New Grade");
                        getSelectedValue(document.getElementById('kId').options[document.getElementById('kId').selectedIndex].value);


});

$(document).on('click', '.update', function(){
  var user_id = $(this).attr("id");
  console.log(user_id);
  $.ajax({
   url:"fetch_single_all.php",
   method:"POST",
   data:{fetchGradeSingle : "1",grade_id:user_id},
   beforeSend:function(){
            $('.update').text('Processing...');
            $('.update').attr('disabled', 'disabled');
          },
   dataType:"json",
   success:function(data)
   {
    enableBtn("Edit");

       console.log(data);
    $('#eventModal').modal('show');
    
    $('#gradeName').val(data.grade_name);
        $('#kId').val(data.kId);

            $('#kId').attr('disabled', 'disabled');

    $('.modal-title').text("Edit Grade Detail");
    $('#user_id').val(user_id);
    $('#kIdH').val(data.kId);

    $('#action').val("Edit");
    $('#operation').val("EditGrade");
                            getSelectedValue(document.getElementById('kId').options[document.getElementById('kId').selectedIndex].value);

   }
  })
 });



 function enableBtnDelete(){
            $('.delete').text("delete");
            $('.delete').attr('disabled', false);
          }
   


 $(document).on('click', '.delete', function(){
     console.log("delete");
  var user_id = $(this).attr("id");
  console.log(user_id);
    Swal.fire({
        title: 'Are you sure delete this?',
        text: "If you delete this , the record will be gone forever",
        type: 'warning',
        showCancelButton: true,

        confirmButtonColor: 'red',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete this!'
    }).then((result) => {
    if (result.value) {
        
        $.ajax({
            url:"insert_all_edit.php",
            method:"POST",
            data:{user_id:user_id,deleteGrade: "1"},
            beforeSend:function(){
            $('.delete').text('Processing...');
            $('.delete').attr('disabled', 'disabled');
          },
            success:function(data)
            {
                if(data == "grade existed"){
                        Swal.fire({
                       title: 'Error Deleting Record!',
        text: "This grade has student or teacher existing inside,please move them to new grade before deleting this ",
        type: 'error'
            });
                }else if(data.includes("Error") == false){
                    Swal.fire({
        title: 'Grade Deleted!',
        text: "This record has been deleted successfully",
        type: 'success'
            });
            dataTable.ajax.reload();
                }else{
                    Swal.fire({
        title: 'Error Deleting Record!',
        text: "Please try again ",
        type: 'error'
            });
            enableBtnDelete();
                }
                            enableBtnDelete();

                enableBtn("Edit");

            
            }
        });
  }
 });

});

});
});






</script>
