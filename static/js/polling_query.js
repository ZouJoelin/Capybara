

const out_trade_no = document.getElementById("out_trade_no").value

function fetchQuery() {
    fetch('/polling_query?out_trade_no=' + out_trade_no)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('请求失败：' + response.statusText);
            }
        })
        .then(result => {
            console.log("message: ", result.message);
            if (result.message == 'SUCCESS') {
                document.getElementById("print-order").submit();
                //window.location.href = '/print_file?out_trade_no=' + out_trade_no;
            } else {
                setTimeout(fetchQuery, 5000); // 间隔5秒后再次调用 fetchQuery 函数
            }
        })
        .catch(error => {
            console.error(error);
            setTimeout(fetchQuery, 5000); // 如果请求失败，则间隔5秒后再次调用 fetchQuery 函数
        });
}

fetchQuery(); // 初次调用 fetchQuery 函数

