        // Add a click event to the "Home" link
        document.getElementById('home-link').addEventListener('click', function (e) {
            var confirmLeave = confirm('Are you sure you want to leave this page?');
            if (!confirmLeave) {
                e.preventDefault();
            }
        });

        $(document).ready(function () {
            // Function to calculate the amount for a row
            function calculateAmount(row) {
                const qty = parseInt(row.find('input[name="qty[]"]').val()) || 0;
                const price = parseInt(row.find('input[name="price[]"]').val()) || 0;
                const amount = qty * price;
                row.find('.amnt').val(amount);
            }

            function calculateTotal() {
                let total = 0;
                $('input[name="qty[]"]').each(function () {
                    const qty = parseInt($(this).val()) || 0;
                    const row = $(this).closest('tr');
                    const price = parseInt(row.find('input[name="price[]"]').val()) || 0;
                    const amount = qty * price;
                    total += amount;
                });
                $('#totalAmount').val('Rs. ' + total);
            }

            // Function to add a new row
            function addRow() {
                const template = $('#dynamic-row-template').clone();
                template.find('input').val('');
                $('#details table tr:last').before(template);
            }


            function generateSerialNumbers() {
                const rows = document.getElementsByClassName('sr-no');

                // Start from 1 to skip the header row
                for (let i = 0; i < rows.length; i++) {
                    rows[i + 1].textContent = i + 1; // Set the serial number
                }
            }

            // Call the function to generate serial numbers


            $('#add-row').click(function () {
                addRow();
                generateSerialNumbers();
            });

            // Calculate amounts when input fields change
            $(document).on('input', 'input[name="qty[]"], input[name="price[]"]', function () {
                calculateAmount($(this).closest('tr'));
                calculateTotal();
            });

            generateSerialNumbers();
        });