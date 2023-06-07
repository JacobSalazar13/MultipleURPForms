function showDropDownQuestions(event) {
    var dropdownId = $(event.target).data('dropdown');
    var dropdown = $('#' + dropdownId);
    dropdown.toggle();

    // If dropdown is visible, add hidden input with label text.
    // If not, remove it.
    if (dropdown.is(':visible')) {
        dropdown.find('input').attr('required', true);

        // Create hidden input with label text
        var labelText = $('label[for="' + dropdownId + '"]').text();
        var hiddenInput = $('<input>').attr({
            type: 'hidden',
            name: dropdownId + '_label',
            value: labelText
        });
        
        // Append hidden input to form
        $('form').append(hiddenInput);
    } else {
        dropdown.find('input').removeAttr('required');
        
        // Remove hidden input
        $('input[name="' + dropdownId + '_label"]').remove();
    }
}
