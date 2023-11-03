// Add a click event to the "Home" link
document.getElementById('home-link').addEventListener('click', function (e) {
    var confirmLeave = confirm('Are you sure you want to leave this page?');
    if (!confirmLeave) {
        e.preventDefault();
    }
});

function calculateAmount() {
    let total_earn = 0;
    let total_deduct = 0;

    // Loop through all rows with the specified name attributes
    $('input[name="earn_amount[]"]').each(function () {
        const earn_amount = parseInt($(this).val()) || 0;
        total_earn += earn_amount;
    });

    $('input[name="deduct_amount[]"]').each(function () {
        const deduct_amount = parseInt($(this).val()) || 0;
        total_deduct += deduct_amount;
    });

    const netTotal = total_earn - total_deduct;

    // Update the total fields
    $('#totalEarn').val('Rs. ' + total_earn);
    $('#totalDeduct').val('Rs. ' + total_deduct);
    $('#netTotal').val('Rs. ' + netTotal);
}


// Function to add a new row
function addRow() {
    const template = $('#dynamic-row-template').clone();
    template.removeAttr('id').show();
    template.find('input[type="text"], input[type="number"]').val('');
    $('#sal-desc-table tr').eq(-5).after(template);
}

$(document).ready(function () {
    $('#add-row').click(function () {
        addRow();
    });

    // Calculate amounts when input fields change
    $(document).on('input', 'input[name="earn_amount[]"], input[name="deduct_amount[]"]', function () {
        const row = $(this).closest('tr');
        calculateAmount(row);
    });
});

