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

