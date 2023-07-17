const button_2 = document.querySelector('button');
const email = document.getElementById('formemail');
const fullname = document.getElementById('formname');
const school = document.getElementById('formschool');
const bulk = document.getElementById('b');
const errorElement = document.getElementById('email_error');
const errorElement_0 = document.getElementById('fullname_error');
const errorElement_1 = document.getElementById('school_error');
const errorElement_2 = document.getElementById('bulk_error');
let emailmessages = [];
let namemessages = [];
let schoolmessages = [];
let bulkmessages = [];


button_2.addEventListener('click', (e) => {
  emailmessages = [];
  namemessages = [];
  schoolmessages = [];
  bulkmessages = [];


  if(email.value === '' || email.value === null){
    emailmessages.push('*Email is required');
  }

  if(fullname.value === '' || fullname.value === null){
    namemessages.push('*Full Name is required');
  }
  if(school.value === '' || school.value === null){
    schoolmessages.push('*School Name is required');
  }

  if(bulk.checked === false){
    bulkmessages.push('*Answer is required');
  }


  if (emailmessages.length > 0 || namemessages.length > 0 || schoolmessages.length > 0 || bulkmessages.length > 0){
    e.preventDefault();
    errorElement.innerText = emailmessages.join(', ');
    errorElement_0.innerText = namemessages.join(', ');
    errorElement_1.innerText = schoolmessages.join(', ');
    errorElement_2.innerText = bulkmessages.join(', ');
  }
});

const form = document.getElementById('multi-page-form');
const pay = document.getElementById('pay');
let paymessages = [];
const errorElement_3 = document.getElementById('pay_error');
const options = document.querySelectorAll('input[id^="option"]');

const course = document.getElementById('option');
let optionmessages = [];
const errorElement_4 = document.getElementById('option_error');

form.addEventListener('submit', (e)=>{
  paymessages = [];
  optionmessages = [];
  
  if(document.querySelector('input[name="payment"]:checked') === null){
    paymessages.push('*Payment is required');
}

  let isOptionSelected = false; // Flag variable

  // Iterate over the options checkboxes
  options.forEach((checkbox) => {
    if (checkbox.checked) {
      isOptionSelected = true; // Set the flag to true if any checkbox is selected
    }
  });

  if (!isOptionSelected) {
    optionmessages.push('*Order is required');
  }

  if (paymessages.length > 0 || optionmessages.length > 0 ){
    e.preventDefault();
    errorElement_3.innerText = paymessages.join(', ');
    errorElement_4.innerText = optionmessages.join(', ');
  }

});


function showDropDownQuestions(event) {
  var dropdownId = $(event.target).data('dropdown');
  var dropdown = $('#' + dropdownId);
  dropdown.toggle();

  // If dropdown is visible, mark the text input as required
  if (dropdown.is(':visible')) {
    dropdown.find('input[type="text"]').prop('required', true);
  } else {
    dropdown.find('input[type="text"]').prop('required', false);
  }

  // If dropdown is visible, mark the hidden input as required
  if (dropdown.is(':visible')) {
    dropdown.find('input[name="hiddenfield"]').prop('required', true);
  } else {
    dropdown.find('input[name="hiddenfield"]').prop('required', false);
  }
}

// Validation on form submission
$('form').submit(function (event) {
  var dropdowns = $('.questions:visible');
  var emptyInputs = dropdowns.find('input[type="text"]').filter(function() {
    return !this.value.trim();
  });

  if (emptyInputs.length > 0) {
    // Prevent form submission if any text input is empty
    event.preventDefault();
    alert('Please complete all the required fields.');
  }
});


var currentPage = 1;
var totalPage = 2; // Update this value if you add more pages

function nextPage() {
  if (currentPage < totalPage) {
      document.getElementById("page-" + currentPage).style.display = "none";
      currentPage++;
      document.getElementById("page-" + currentPage).style.display = "block";
  }
}

function previousPage() {
  if (currentPage > 1) {
      document.getElementById("page-" + currentPage).style.display = "none";
      currentPage--;
      document.getElementById("page-" + currentPage).style.display = "block";
  }
}

function checkBulk() {
  const selectedValue = document.querySelector('input[type="radio"][name="bulk"]:checked').value;
  
  if (selectedValue === "I am a student or parent") {
      document.getElementById("bulkResults").innerHTML = "Bulk discounts are only available to teachers/schools that have a minimum of 10 students per subject. Please visit <a href='https://www.ultimatereviewpacket.com'>www.ultimatereviewpacket.com</a> to buy an individual copy of the Ultimate Review Packet.";
      document.getElementById("formQuestions").style.display = "none";
      document.getElementById("multi-page-form").submit(); // Hide the form
  } else if (selectedValue === "I am a teacher or school employee and I want to request a free teacher trial") {
      document.getElementById("bulkResults").innerHTML = "Please fill out this form to request a free teacher trial: <a href='https://forms.gle/vDuq13XEnBLhkf7i6'>https://forms.gle/vDuq13XEnBLhkf7i6</a>";
      document.getElementById("formQuestions").style.display = "none";
      document.getElementById("multi-page-form").submit(); // Hide the form
  } else {
    if (email.value === '' || email.value === null) {
      emailmessages.push('*Email is required');
    }
    if (fullname.value === '' || fullname.value === null) {
      namemessages.push('*Full Name is required');
    }
    if (school.value === '' || school.value === null) {
      schoolmessages.push('*School Name is required');
    }

    if (emailmessages.length > 0 || namemessages.length > 0 || schoolmessages.length > 0) {
      e.preventDefault();
      errorElement.innerText = emailmessages.join(', ');
      errorElement_0.innerText = namemessages.join(', ');
      errorElement_1.innerText = schoolmessages.join(', ');
    } 
    else {
      nextPage(); // Call nextPage() function when other options are selected
  }
}
  
  document.getElementById("bulkResults").style.display = "block";
  }
  function goToTeacherWS() {
      // Check if the button with id="teacherws" is pressed
      var teacherWSButton = document.getElementById("teacherws");
      if (teacherWSButton) {
        // Redirect to the specified link
        window.location.href = "https://docs.google.com/forms/d/e/1FAIpQLSc3ntjYvBwZUykFPv8q9JbkFgI0TD1IbCUwAUBbOHkTMKwR5Q/viewform";
      }
    }


function validateForm() {
  // Check if the form is valid
  if (document.getElementById("multi-page-form").checkValidity()) {
      // If the form is valid, return true to submit the form
      return true;
  } else {
      // If the form is invalid, display an error message or perform any other desired action
      alert("Please fill in all required fields.");
      return false; // Prevent the form from submitting
  }
  }
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('input[name="payment"]').forEach((el) => {
      el.addEventListener('change', function() {
      document.getElementById('purchaseOrderInput').style.display = (this.id === 'purchaseOrder' && this.checked) ? 'block' : 'none';
      });
  });
  });


