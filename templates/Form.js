function showDropDownQuestions(event) {
    var button = event.target;
    var dropdownId = button.getAttribute('data-dropdown');

    var dropdown = document.getElementById(dropdownId);
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
}