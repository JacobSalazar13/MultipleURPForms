function showDropDownQuestions() {
    var buttonId = document.getAttribute('type'); // Get the ID of the clicked button
    var dropdownId = 'dropdownQuestions-' + buttonId.split('-')[1]; // Construct the ID of the corresponding dropdown

    var dropdown = document.getElementById(dropdownId);
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
}