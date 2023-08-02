async function GetOrdersInfo(start, end){ // this function get a week ago orders info in whole app
    let response = await fetch(`/admin/api/AllOrders/?from=${start.toString()}&end=${end.toString()}`, {
        method:"GET",
        headers :{
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    let data = (await response).json()
    return data
}


async function GetSectionOrdersInfo(start, end){ // this function get each section a week ago orders info in whole app

    let response = await fetch(`/admin/api/AllOrders/Sections/?from=${start.toString()}&end=${end.toString()}`, {
        method:"GET",
        headers :{
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    let data = (await response).json()
    return data
}


window.addEventListener("DOMContentLoaded", async (e)=>{
    const Today = moment().toISOString();
    const PreWeek = moment().subtract(1, 'week').toISOString();

    let GetOrdersInfo_response = await GetOrdersInfo(Today, PreWeek);
    let GetSectionOrdersInfo_response = await GetSectionOrdersInfo(Today, PreWeek);

    let xValues = []
    let yValues = []
    for (const value of GetOrdersInfo_response.data) {
        for (const valueElement in value) {
            xValues.push(valueElement)
            yValues.push(value[valueElement])
        }
    }

    create_chart(
        document.querySelector("#last-week-orders"),
        "line",
        xValues,
        yValues,
        "سفارشات هفته اخیر در کل بخش ها",
        [65,120,195]
    )

    xValues = []
    yValues = []
    for (const Value of GetSectionOrdersInfo_response.data) {
        xValues.push(Value["section_name"])
        yValues.push(Value["orders_count"])
    }

    create_chart(
        document.querySelector("#one-week-orders-section"),
        "line",
        xValues,
        yValues,
        "سفارشات هفته اخیر بر اساس بخش ها",
        [65,120,195]
    )


})

function create_chart(ctx, type, xValues, yValues, label, borderColor){
     let data = {
      labels: xValues,
      datasets: [{
        label: label,
        data: yValues,
        fill: false,
        borderColor: `rgb(${borderColor[0]}, ${borderColor[1]}, ${borderColor[2]})`,
        tension: 0.1
      }]
    };
      const config = {
          type: type,
          data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
    };

    return new Chart(ctx, config)
}