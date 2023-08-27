

const out_trade_no = document.getElementById("out_trade_no").value

async function fetchQuery() {
    try {
        let response = await fetch('/polling_query?out_trade_no=' + out_trade_no);
        if (!response.ok) {
            let errorJSON = await response.json();
            throw errorJSON;
        }
        let parsedJSON = await response.json();
        let message = parsedJSON.message;
        if (message == 'SUCCESS') {
            document.getElementById("print-order").submit();
            //window.location.href = '/print_file?out_trade_no=' + out_trade_no;
        } else {
            setTimeout(fetchQuery, 2000); // 间隔5秒后再次调用 fetchQuery 函数
        }
    } catch (errorJSON) {
        let error_message = await errorJSON.error_message;
        setTimeout(fetchQuery, 2000); // 如果请求失败，则间隔5秒后再次调用 fetchQuery 函数

    }
}

fetchQuery(); // 初次调用 fetchQuery 函数

