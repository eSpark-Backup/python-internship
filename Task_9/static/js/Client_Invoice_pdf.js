var originalContent = document.body.innerHTML; // Store the original content

function my_print(p_id) {
    var to_print = document.getElementById(p_id).innerHTML;
    document.body.innerHTML = to_print;
    window.print();
    document.body.innerHTML = originalContent;
}

function generateSerialNumbers() {
    const rows = document.getElementsByClassName('sr-no');

    // Start from 1 to skip the header row
    for (let i = 0; i < rows.length; i++) {
        rows[i + 1].textContent = i + 1; // Set the serial number
    }
}

// Call the function to generate serial numbers
generateSerialNumbers();


// Call the function to generate serial numbers
generateSerialNumbers();