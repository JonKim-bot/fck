<?php include 'topNavParent.php'?>
<script>
         function dateValidation1(){
        var from_date = $('#from_date1').val();
    var to_date = $('#to_date1').val();
    if(from_date > to_date){
        $('#searchBtn').hide();
        $('#error_to_date1').show();

        $('#error_to_date1').html("From date cannot bigger than To date");
    }else{
        $('#searchBtn').show();
        $('#error_to_date1').hide();

    }
 }
 
        </script>
                <main>
                    <div class="container-fluid">
                    <div style="margin:80px"></div>
                   
                    <div class="card-header text-center">
                        <div class="row">
                        <div class="col-md-9">
                        <h1 class="mt-4 text-center">Student Attendance Details</h1>
                    <p>Below are yours children attendance details,if you wish to upload an mc or letter , click the upload button and submit and you will need to wait for admin or teacher approval , usually it takes 3 working days to verify your submitted information</p>
                        </div>

                        <div class="col-md-3">
                        
                        <button type="button" class="btn btn-info" id="search_button">Search By Date</button>
                                        <a class="btn btn-warning btn-block" href="viewChildren.php" >View Reports and Charts</a>

                        <br>
                        </div>
                        </div>
                        </div>
                        
                        <div class="row">
                            
                        </div>
                        <div class="card mb-4">

                        <div class="card-header"><i class="fas fa-table mr-1"></i>Attendance Detail</div>

                            <div class="card-body">
                                
                                <div class="table-responsive">
                                   

                                    <table class="table table-bordered table-striped" id="dataTable" width="100%" cellspacing="0">
                                        <thead>
                                            <tr>
                                            <th>View detail</th>

                                            <th>Student Name</th>
                                       
                                            <th>Date</th>
                                            <th>Status</th>
                                            <th>Upload Mc Or Letter</th>  


                                 
          
                                            </tr>
                                        </thead>
                                        
                                     

                                    
                                      


                                        <tfoot>
                                            <tr>
                                             
                                            <th>View detail</th>

                                            <th>Student Name</th>
                                       
                                            <th>Date</th>
                                            <th>Status</th>
                                            <th>Upload Mc Or Letter</th>  


                                 


                                            </tr>
                                        </tfoot>
                                        
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
                <footer class="py-4 bg-light mt-auto">
                    <div class="container-fluid">
                        <div class="d-flex align-items-center justify-content-between small">
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
    </div>

    <div class="modal fade" id="viewModal"  >
  <div class="modal-dialog modal-lg" style="background:#282828;border-radius:3%">
    <div class="modal-content">

      <!-- Modal Header -->
      <div class="modal-header">
        <h4 class="modal-title">Student Attendance Details</h4>
        <button type="button" class="close" data-dismiss="modal">&times;</button>
      </div>

      <!-- Modal body -->
      <div class="modal-body" style="background:#282828;border-radius:1%" id="student_attendance_details">
      </div>

      <!-- Modal footer -->
      <div class="modal-footer">


        <button type="button" class="btn btn-danger btn-sm" data-dismiss="modal">Close</button>
      </div>

    </div>
  </div>
</div>



    <div id="eventModal" class="modal fade">
 <div class="modal-dialog">
  <form method="post" id="event_form" enctype="multipart/form-data">
   <div class="modal-content">
    <div class="modal-header">
    <h4 class="modal-title">Upload MC</h4>

     <button type="button" class="close" data-dismiss="modal">&times;</button>
    </div>
    <div class="modal-body">
        <p id="lblDecription" style="text-align:center"></p>
    <div id="mcImageDiv">
     <label>Uploaded MC</label>
     <img class="img-thumbnail" alt="mcImage" id="mcImage">
     <br />
     <label class="badge badge-danger" id="mcStatus">Awaiting Approve</label>
     </div>
<div class="form-group" id="attendanceLetter">
    <label><b>Letter Sample :</b></label>
    <textarea class="form-control" name="attendanceLetterText" id="attendanceLetterText" rows="8"></textarea>
    <label class="badge" style="background:red;color:white" id="letterStatus">Awaiting Approve</label>

  </div>
        
     <label id="lblImage"><b>Select Image :</b></label>
     <input type="file" name="user_image" id="user_image" />
     <span id="user_uploaded_image"></span>
     <input type="hidden"  name="user_id" id="user_id" />
     <input type="hidden" name="operation" id="operation" />
     <input type="submit" name="action" id="action" class="btn btn-success" value="Add" />
     <button type="button" class="btn btn-warning" data-dismiss="modal">Close</button>
    </div>
    
   </div>
  </form>
 </div>
</div>

<div class="modal fade" id="dateModal">
  <div class="modal-dialog" style="background:#282828;border-radius:1%">
    <div class="modal-content">

      <!-- Modal Header -->
      <div class="modal-header">
      <h4 class="modal-title">Search By Date</h4>
        <button type="button" class="close" data-dismiss="modal">&times;</button>
      </div>

      <!-- Modal body -->
      <div class="modal-body" style="background:#282828;border-radius:1%">
                               <p class="text-center text-white">Select a range of date to filter out the data</p>
        <div class="form-group">
        
        
          <div class="input-daterange">
          <label><b>From Date :</b></label>

            <input type="date" name="from_date1" id="from_date1" class="form-control" placeholder="From Date" onchange="dateValidation1()"  />
            <span id="error_from_date1" class="text-danger"></span>
            <br />
            <div id="showTodate">
            <label><b>To Date :</b></label>

            <input type="date" name="to_date1" id="to_date1" class="form-control" placeholder="To Date" onchange="dateValidation1()"  />
            <span id="error_to_date1" class="text-danger"></span>
            </div>
          </div>
        </div>
      </div>
      <!-- Modal footer -->
      <div class="modal-footer">

        <div class='btn-toolbar text-center' style="display:block;margin:auto">
    <div class='btn-group'>

    <button type="button" name="searchBtn" id="searchBtn" class="btn btn-success btn-sm">Search By Date</button>
        <button type="button" class="btn btn-danger btn-sm" data-dismiss="modal">Close</button>

     </div>
    
    </div>
      </div>

    </div>
  </div>


</div>


    
   

<!--  -->
<?php include 'footerParent.php'; ?>

        <script>
            $(document).ready(function() {

                document.getElementById('from_date1').max = new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString().split("T")[0];
    document.getElementById('to_date1').max = new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString().split("T")[0];
    $(document).on('click', '#search_button', function(){
    
  
       $('.modal-title').text("Search By Date");

    $('#dateModal').modal('show');


    $('#error_to_date1').text('');
    $('#error_from_date1').text('');


  });
  $('#dateModal').on('hidden.bs.modal', function () {
    // do something
    console.log("clear field");
    $("input[type=date]").val("");

    $('#searchBtn').show();

});
  $('#searchBtn').click(function(){
    var from_date = $('#from_date1').val();
    var to_date = $('#to_date1').val();

    var error = 0;
   
    if(from_date == '')
    {
        $('#from_date1').focus();
      $('#error_from_date1').text('From Date is Required');
      error++;
    }
    else
    {
      $('#error_from_date1').text('');
    }

    if(to_date == '')
    {
                $('#to_date1').focus();

      $('#error_to_date1').text("To Date is Required");
      error++;
    }
    else
    {
      $('#error_to_date1').text('');
    }

    if(error == 0)
    {
      
   $('#dataTable').DataTable().destroy();
   fetch_data('yes', from_date, to_date);
   $('#dateModal').modal('hide');


    
    }
     
      
     
    });

    fetch_data('no');

function fetch_data(is_date_search, start_date='', end_date='')
{console.log(start_date);
 console.log(end_date);
 var parentId = "<?php echo $parentId?>";
               console.log(parentId + "is parentid");
               var table =  $('#dataTable').DataTable({
                "processing":true,

                        "serverSide":true,
                        "order":[],
                        "ajax":{
                        url:"fetchAttendance.php",
                        type:"POST",
                        'data': {
                            parentId : parentId,is_date_search:is_date_search, start_date:start_date, end_date:end_date
                            // post data to ajax qr page
                            },
                        "columnDefs":[
                        {
                            "targets":[0, 4],
                            "orderable":false,
                        },
                        ],
                        }

                    //    dom: 'Bfrtip',
                    //    buttons: [
                    //        'copyHtml5',
                    //        'excelHtml5',
                    //        'csvHtml5',
                    //        'pdfHtml5',
                    //        'print',
                    //        'reload'

                   
                            

                    //    ]        
                 
                    });
}
function enableBtns(){
    $('.viewDetail').text('View Details');
            $('.viewDetail').attr('disabled', false);
            $('.update').text('Upload MC');
            $('.update').attr('disabled', false);
            $('.uploadLetter').text('Upload Letter');
            $('.uploadLetter').attr('disabled', false);
            $('.viewLetter').text('View Ltter');

            $('.viewLetter').attr('disabled', false);
            $('#action').val('Submit');
            
            $('#action').attr('disabled', false);
          

}
                $(document).on('click', '.viewDetail', function(){
    user_id = $(this).attr('id');
    $.ajax({
      url:"fetchSingleAttendance.php",
      method:"POST",
      data:{viewStudentAttendance : 1, user_id:user_id},
      beforeSend:function(){
            $('.viewDetail').text('Processing...');
            $('.viewDetail').attr('disabled', 'disabled');
          },

      success:function(data)
      {
          enableBtns();
        $('#viewModal').modal('show');
        $('#student_attendance_details').html(data);
    
      }
    });
  });
//                 $.fn.dataTable.ext.buttons.reload = {
//     text: 'Reload Table ',
//     action: function ( e, dt, node, config ) {
//         location.reload();
//     }
//     add reload function to button

// };
//TODO change it to dynamic parent id 
var parentId = "<?php echo $parentId ?>" ;
$(document).on('submit', '#event_form', function(event){
  event.preventDefault();//this method will stop summit form data
  var extension = $('#user_image').val().split('.').pop().toLowerCase();
  if(extension != '')
  {
   if(jQuery.inArray(extension, ['gif','png','jpg','jpeg']) == -1)
   {
    alert("Invalid Image File");
    $('#user_image').val('');
    return false;

   }
  } 
 
    let formData = new FormData(this);
    console.log(formData.values() + "is form data");
    var queryString = $('#event_form').serialize();
   // alert(queryString);
   $.ajax({
    
    url:"uploadMC.php",
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
        enableBtns();
        if(data == "update letter success"){
            Swal.fire({
                    title: 'Letter Submitted',
                    text: "Please wait for admin to approved!",
                    type: 'success'
                    })
        }
        if(data == "update mc success"){
            Swal.fire({
                    title: 'MC Submitted',
                    text: "Please wait for admin to approved!",
                    type: 'success'
                    })
        }
        if(data == "please upload an image"){
            Swal.fire({
                    title: 'Error',
                    text: "Please upload an MC!",
                    type: 'error'
                    })
        }

     console.log(data);
     $('#event_form')[0].reset();

     $('#eventModal').modal('hide');
     //hide the table after success
       $('#dataTable').DataTable().ajax.reload(null, false);

    }
   });

 });
               
           
                    

                    $(document).on('click', '.update', function(){
                        var user_id = $(this).attr("id");
  console.log(user_id);
  $.ajax({
   url:"fetchSingleAttendance.php",
   method:"POST",
   data:{uploadMcLetter : 1 ,attendanceId:user_id},
   
   dataType:"json",
   beforeSend:function(){
            $('.update').text('Processing...');
            $('.update').attr('disabled', 'disabled');
          },
   success:function(data)
   {
       enableBtns();
    $('#eventModal').modal('show');
    $('.modal-title').text("Upload Mc");
    $('#user_image').show();

$('#user_uploaded_image').show();
    $('#user_id').val(user_id);
    $('#user_uploaded_image').html(data.user_image);
    $('#action').val("Upload MC");
    $('#operation').val("uploadMC");
    $('#attendanceLetter').hide();
    $('#attendanceLetterText').prop('disabled', false);
        $('#lblDecription').text("Note : Your MC image must contain a clear date , and also reason of leave");

    $('#lblImage').show();
    $('#action').show();
    $('#mcImageDiv').hide();

    $("#mcStatus").hide();


   }
  })
 });
 $(document).on('click', '.uploadLetter', function(){
                    var user_id = $(this).attr("id");
    console.log(user_id);
    
    $.ajax({
   url:"fetchSingleAttendance.php",
   method:"POST",
   data:{attendanceId:user_id,getLetterDetail : "1",parentId  : parentId},
   dataType:"json",
   beforeSend:function(){
            $('.uploadLetter').text('Processing...');
            $('.uploadLetter').attr('disabled', 'disabled');
          },
   success:function(data)
   {
       enableBtns();
               $('#lblDecription').text("Note : Your letter must contain a clear date , and also reason of leave");

    $('#eventModal').modal('show');
    $('.modal-title').text("Submit Letter");
    $('#user_id').val(user_id);
    $('#user_image').hide();

    $('#user_uploaded_image').hide();
    $('#action').val("Submit");
    $('#operation').val("uploadLetter");
    $('#attendanceLetter').show();
    $('#action').show();
    $("#letterStatus").hide();

    $('#mcImageDiv').hide();


    $('#attendanceLetterText').prop('disabled', false);

    var studentName = data.student_name;
    var parentName = data.parent_name;
    var dateLetter = data.dateLetter;
    var txtLetter = "Dear Mr Teacher or Admin,\n\nPlease excuse my son/daughter "+studentName+" for being absent last "+dateLetter+". He / She is sick with ____________(illness Or other reason).\n\nThank you very much for your consideration.\n\nVery truly yours,\n\n"+parentName+". ";
    $('#attendanceLetterText').html(txtLetter);
    $('#lblImage').hide();




   }
                                });
                                
   


  });

  $(document).on('click', '.viewLetter', function(){
                    var user_id = $(this).attr("id");
    console.log(user_id);
    
    $.ajax({
   url:"fetchSingleAttendance.php",
   method:"POST",
   data:{attendanceId:user_id,viewLetterOrImageMC : "1"},
   beforeSend:function(){
            $('.viewLetter').text('Processing...');
            $('.viewLetter').attr('disabled', 'disabled');
          },
   dataType:"json",
   success:function(data)
   {
       enableBtns();
    $('#eventModal').modal('show');
    $('.modal-title').text("View Letter");
    $('#user_id').val(user_id);
    $('#user_image').hide();

    $('#user_uploaded_image').hide();
    $('#action').val("Submit");
    $('#action').hide();
    $('#mcImageDiv').hide();
        $('#lblDecription').text("Note : Its usually takes 2 to 3 working days for admin approval.");

    $('#operation').val("uploadLetter");
    $('#attendanceLetter').show();
    var letter = data.letter;
    $('#attendanceLetterText').prop('disabled', true);
    $('#attendanceLetterText').html(letter);
    $("#letterStatus").show();

    if(data.adminConfirmation == "unavalible"){

    $('#letterStatus').html("Pending approval");

    $("#letterStatus").css("background-color", "red");
    $("#letterStatus").css("color", "white");

    }else if(data.adminConfirmation == "1"){
        $('#letterStatus').html("approved");

$("#letterStatus").css("background-color", "green");
$("#letterStatus").css("color", "white");

    }
    else if(data.adminConfirmation == "0"){
        $('#letterStatus').html("disapproved");
        $("#letterStatus").css("background-color", "red");
    $("#letterStatus").css("color", "white");

    }



    
    $('#lblImage').hide();

   }
                                });
                                
   


  });
  
    $(document).on('click', '.viewMc', function(){
        var user_id = $(this).attr("id");
    console.log(user_id);
    
    $.ajax({
   url:"fetchSingleAttendance.php",
   method:"POST",
   data:{attendanceId:user_id,viewLetterOrImageMC : "1"},
   dataType:"json",
   success:function(data)
   {
    $('#eventModal').modal('show');
    $('.modal-title').text("View Mc");
    $('#user_id').val(user_id);
    $('#user_image').hide();

    $('#user_uploaded_image').hide();
    $('#action').val("Submit");
    $('#action').hide();
    $('#mcImageDiv').show();
        $('#lblDecription').text("Note : it usually takes 2 to 3 working days for getting approval");

    $('#operation').val("uploadLetter");
    $('#lblImage').hide();
    $("#mcStatus").show();

    $('#attendanceLetter').hide();
    $("#mcImage").attr("src",data.image);
    $('#attendanceLetterText').prop('disabled', true);
   // $('#attendanceLetterText').html(letter);
  
    if(data.adminConfirmation == "unavalible"){

        $('#mcStatus').html("Pending approval");

$("#mcStatus").css("background-color", "red");
$("#mcStatus").css("color", "white");

}else if(data.adminConfirmation == "1"){
    $('#mcStatus').html("approved");

$("#mcStatus").css("background-color", "green");
$("#mcStatus").css("color", "white");

}
else if(data.adminConfirmation == "0"){
    
    $('#mcStatus').html("Disapproved");

$("#mcStatus").css("background-color", "red");
$("#mcStatus").css("color", "white");

}
}
    });

    });

  $(document).on('click', '.viewMC', function(){
                    var user_id = $(this).attr("id");
    console.log(user_id);
    
    $.ajax({
   url:"fetchSingleAttendance.php",
   method:"POST",
   data:{attendanceId:user_id,viewLetterOrImageMC : "1"},
   dataType:"json",
   success:function(data)
   {
    $('#eventModal').modal('show');
    $('.modal-title').text("View Mc");
    $('#user_id').val(user_id);
    $('#user_image').hide();

    $('#user_uploaded_image').hide();
    $('#action').val("Submit");
    $('#action').hide();
    $('#mcImageDiv').show();
        $('#lblDecription').text("Note : it usually takes 2 to 3 working days for getting approval");

    $('#operation').val("uploadLetter");
    $('#lblImage').hide();
    $("#mcStatus").show();

    $('#attendanceLetter').hide();
    $("#mcImage").attr("src",data.image);
    $('#attendanceLetterText').prop('disabled', true);
   // $('#attendanceLetterText').html(letter);
  
    if(data.adminConfirmation == "unavalible"){

        $('#mcStatus').html("Pending approval");

$("#mcStatus").css("background-color", "red");
$("#mcStatus").css("color", "white");

}else if(data.adminConfirmation == "1"){
    $('#mcStatus').html("approved");

$("#mcStatus").css("background-color", "green");
$("#mcStatus").css("color", "white");

}
else if(data.adminConfirmation == "0"){
    
    $('#mcStatus').html("Disapproved");

$("#mcStatus").css("background-color", "red");
$("#mcStatus").css("color", "white");

}

   }
                                });
                                
   


  });


                            });


                   
                </script>
                
                   

             