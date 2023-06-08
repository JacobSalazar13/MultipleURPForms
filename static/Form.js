function showDropDownQuestions(event) {
    var dropdownId = $(event.target).data('dropdown');
    var dropdown = $('#' + dropdownId);
    dropdown.toggle();

    // If dropdown is visible, add hidden input with the value of another input.
    // If not, remove it.
    if (dropdown.is(':visible')) {
        dropdown.find('input').attr('required', true);

        // Get value of the other input field
        var inputValue = dropdown.find('input[name="hiddenfield"]').val(); // Replace 'your_input_name' with the name of the input you want to fetch the value from.

        // Create hidden input with the fetched value
        var hiddenInput = $('<input>').attr({
            type: 'hidden',
            name: dropdownId + '_hidden',
            value: inputValue
        });
        
        // Append hidden input to form
        $('form').append(hiddenInput);
    } else {
        dropdown.find('input').removeAttr('required');
        
        // Remove hidden input
        $('input[name="' + dropdownId + '_hidden"]').remove();
    }
}

var currentPage = 1;
    var totalPage = 3; // Update this value if you add more pages

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
        } else if (selectedValue === "I am a teacher or school employee and I want to request a free teacher trial") {
          document.getElementById("bulkResults").innerHTML = "Please fill out this form to request a free teacher trial: <a href='https://forms.gle/vDuq13XEnBLhkf7i6'>https://forms.gle/vDuq13XEnBLhkf7i6</a>";
        } else {
          nextPage(); // Call nextPage() function when other options are selected
          document.getElementById("formQuestions").style.display = "none"; // Hide the form
        }
      
        document.getElementById("bulkResults").style.display = "block";
      }
      
const submitButton = document.getElementById("submitButton");

// Check if the current page is page 2
if (currentPage === 2) {
// Show the submit button
submitButton.style.display = "block";
} else {
// Hide the submit button
submitButton.style.display = "none"; }