        // Add a click event to the "Home" link
        document.getElementById('home-link').addEventListener('click', function (e) {
            var confirmLeave = confirm('Are you sure you want to leave this page?');
            if (!confirmLeave) {
                e.preventDefault();
            }
        });
        $(document).ready(function () {
            // Function to calculate the amount for a row
            function calculateAmount() {
                $('tr.dynamic-row').each(function (index) {
                    const qty = parseInt($(this).find('input[name="qty[]"]').val()) || 0;
                    const price = parseInt($(this).find('input[name="price[]"]').val()) || 0;
                    const amount = qty * price;
                    $(this).find('.amnt').val(amount);
                });
                calculateTotal();
            }

            function calculateTotal() {
                let total = 0;
                $('tr.dynamic-row').each(function (index) {
                    const qty = parseInt($(this).find('input[name="qty[]"]').val()) || 0;
                    const price = parseInt($(this).find('input[name="price[]"]').val()) || 0;
                    const amount = qty * price;
                    total += amount;
                });
                $('#totalAmount').val('Rs. ' + total);
            }

            // Function to add a new row
            function addRow() {
                const template = $('#dynamic-row-template').clone();
                template.removeAttr('id').addClass('dynamic-row').show();
                template.find('.sr-no').text($('tr.dynamic-row').length + 1);
                $('#details table tr:last').before(template);
            }

            $('#add-row').click(function () {
                addRow();
            });

            // Calculate amounts when input fields change
            $(document).on('input', 'input[name="qty[]"], input[name="price[]"]', function () {
                calculateAmount();
            });

            // Initial row
            addRow();
        });