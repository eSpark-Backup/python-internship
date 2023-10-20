// Add a click event to the "Home" link
document.getElementById('home-link').addEventListener('click', function (e) {
    var confirmLeave = confirm('Are you sure you want to leave this page?');
    if (!confirmLeave) {
        e.preventDefault();
    }
});
// Function to calculate the amount for a row
function calculateAmount(row) {
    const hours = parseInt(row.find('input[name="hours[]"]').val()) || 0;
    const hourlyRate = parseInt(row.find('input[name="hourly_rate[]"]').val()) || 0;
    const amount = hours * hourlyRate;
    row.find('.amount').val(amount);
    calculateTotal();
}

function calculateTotal() {
    let total = 0;
    $('input[name="hours[]"]').each(function () {
        const hours = parseInt($(this).val()) || 0;
        const row = $(this).closest('tr');
        const hourlyRate = parseInt(row.find('input[name="hourly_rate[]"]').val()) || 0;
        const amount = hours * hourlyRate;
        total += amount;
    });
    $('#totalAmount').val('Rs. ' + total);
}

// Function to add a new row
function addRow() {
    const template = $('#dynamic-row-template').clone();
    template.removeAttr('id').show();
    template.find('input[type="text"], input[type="number"]').val('');

    $('#sal-desc-table tr').eq(-3).after(template);
}

$(document).ready(function () {
    $('#add-row').click(function () {
        addRow();
    });

    // Calculate amounts when input fields change
    $(document).on('input', 'input[name="hours[]"], input[name="hourly_rate[]"]', function () {
        const row = $(this).closest('tr');
        calculateAmount(row);
    });
});