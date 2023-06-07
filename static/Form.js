function showDropDownQuestions(event) {
    var dropdownId = $(event.target).data('dropdown');
    var dropdown = $('#' + dropdownId);
    dropdown.toggle();

    // If dropdown is visible, add required attribute to inputs.
    // If not, remove it.
    if (dropdown.is(':visible')) {
        dropdown.find('input').attr('required', true);
    } else {
        dropdown.find('input').removeAttr('required');
    }
}
