// Function to calculate age from date of birth
function calculateAge() {
    const dobInput = document.getElementById('dob');
    const ageInput = document.getElementById('age');
    const dobValue = dobInput.value;

    if (dobValue) {
        const dobDate = new Date(dobValue);
        const today = new Date();
        const age = today.getFullYear() - dobDate.getFullYear();

        // Check if the birthday has occurred this year
        if (today.getMonth() < dobDate.getMonth() || (today.getMonth() === dobDate.getMonth() && today.getDate() < dobDate.getDate())) {
            age--;
        }

        ageInput.value = age + ' Years';
    }
}

// Add an event listener to the Date of Birth input field
const dobInput = document.getElementById('dob');
dobInput.addEventListener('input', calculateAge);




// Function to calculate Total service from joining date and resign date
function calculateTotalService() {
    const joinDate = document.getElementById('join_date');
    const resignDate = document.getElementById('res_date');
    const totalServiceInput = document.getElementById('tot_serv');
    const jdValue = joinDate.value;
    const rdValue = resignDate.value;

    if (jdValue) {
        const jdDate = new Date(jdValue);
        const today = new Date();
        let totalYears = today.getFullYear() - jdDate.getFullYear();
        let totalMonths = today.getMonth() - jdDate.getMonth();

        if (today.getDate() < jdDate.getDate()) {
            totalMonths--;
        }

        if (rdValue) {
            const rdDate = new Date(rdValue);
            totalYears = rdDate.getFullYear() - jdDate.getFullYear();
            totalMonths = rdDate.getMonth() - jdDate.getMonth();
            if (rdDate.getDate() < jdDate.getDate()) {
                totalMonths--;
            }
        }

        if (totalMonths < 0) {
            if (totalYears > 0) {
                totalMonths += 12;
                totalYears--;
            }
            else {
                totalYears = 0 //Example 0ct 2023- Nov 2023 -1 Month, 0 year not possible
            }
        }

        let totalService = '';
        if (totalYears > 0) {
            totalService += totalYears + ' Year';
            if (totalYears > 1) {
                totalService += 's';
            }
            if (totalMonths > 0) {
                totalService += ' ';
            }
        }
        if (totalMonths > 0) {
            totalService += totalMonths + ' Month';
            if (totalMonths > 1) {
                totalService += 's';
            }
        }

        totalServiceInput.value = totalService;
    }
}

// Add event listeners to the Date of Joining and Resignation input fields
const joinDate = document.getElementById('join_date');
const resignDate = document.getElementById('res_date');
joinDate.addEventListener('input', calculateTotalService);
resignDate.addEventListener('input', calculateTotalService);

// Calculate the total service initially in case dates are pre-filled
calculateTotalService();