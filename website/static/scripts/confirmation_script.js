function showConfirmation() {
    // Display a confirmation dialog
    var result = confirm("Are you sure you want to continue?");
    
    // If the user clicks "OK", the form is submitted
    return result;
}

function showConfirmation(message) {
    // Display a confirmation dialog
    var result = confirm(message);
    
    // If the user clicks "OK", the form is submitted
    return result;
}