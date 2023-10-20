var originalContent = document.body.innerHTML; // Store the original content

function my_print(p_id) {
    var to_print = document.getElementById(p_id).innerHTML;
    document.body.innerHTML = to_print;
    window.print();
    document.body.innerHTML = originalContent;
}