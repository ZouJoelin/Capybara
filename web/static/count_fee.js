var total_fee = 0;
function count_fee()
{
    var pages = document.getElementById("pages").value;
    var copies = document.getElementById("copies").value;


    total_fee = pages * 0.125 * copies;    
    document.getElementById("total_fee").innerHTML = total_fee//.toFixed(2);

}