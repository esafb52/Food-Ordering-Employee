function generateRGBString(round) {
   let data = []

    for (let i = 0; i < round; i++){
      const x = Math.floor(Math.random() * 256);
      const y = Math.floor(Math.random() * 256);
      const z = Math.floor(Math.random() * 256);
      data.push(`rgb(${x}, ${y}, ${z})`)
   }
    return data
}


async function GetOrdersInfo(start, end){ // this function get a week ago orders info in whole app
    let response = await fetch(`/admin/api/AllOrders/?from=${start.toString()}&end=${end.toString()}`, {
        method:"GET",
        headers :{
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    let data = (await response).json()
    if (response.status == 200){
        return data
    }
    else{
        return []
    }
}

async function GetAllUsersInfo(){ // this function get all users info by sections
    let response = await fetch(`/admin//api/All/Users/`, {
        method:"GET",
        headers :{
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    let data = (await response).json()
    if (response.status == 200){
        return data
    }
    else{
        return []
    }
}


async function GetSectionOrdersInfo(start, end){ // this function get each section a week ago orders info in whole app

    let response = await fetch(`/admin/api/AllOrders/Sections/?from=${start.toString()}&end=${end.toString()}`, {
        method:"GET",
        headers :{
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    let data = (await response).json()
    if (response.status == 200){
        return data
    }
    else{
        return []
    }
}


window.addEventListener("DOMContentLoaded", async (e)=>{
    const Today = moment().toISOString();
    const PreWeek = moment().subtract(1, 'week').toISOString();

    let GetOrdersInfo_response = await GetOrdersInfo(Today, PreWeek);
    let GetSectionOrdersInfo_response = await GetSectionOrdersInfo(Today, PreWeek);
    let GetAllUsersInfo_response = await GetAllUsersInfo();

    let xValues = []
    let yValues = []
    for (const value of GetOrdersInfo_response.data) {
        for (const valueElement in value) {
            xValues.push(valueElement)
            yValues.push(value[valueElement])
        }
    }

    create_line_chart(
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

    create_line_chart(
        document.querySelector("#one-week-orders-section"),
        "line",
        xValues,
        yValues,
        "سفارشات هفته اخیر بر اساس بخش ها",
        [65,120,195]
    )

    xValues = []
    yValues = []
    for (const Value of GetAllUsersInfo_response.data) {
        xValues.push(Value["section_name"])
        yValues.push(Value["section_users"])
    }

    create_pie_chart(
        document.querySelector("#all_users_info"),
        "pie",
        xValues,
        yValues,
    "کل کاربران سامانه",
    )

})

function create_line_chart(ctx, type, xValues, yValues, label, borderColor){
     let data = {
      labels: xValues,
      datasets: [{
        label: label,
        data: yValues,
        // fill: false,
        borderColor: generateRGBString(xValues.length),
        // backgroundColor: generateRGBString(xValues.length),
        tension: 0.1
      }],
      hoverOffset: 4
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
function create_pie_chart(ctx, type, xValues, yValues, label){
    const data = {
      labels: xValues,
      datasets: [{
        label: label,
        data: yValues,
        backgroundColor: generateRGBString(xValues.length),
        hoverOffset: 4
      }]
    };
     const config = {
      type: 'pie',
      data: data,
    };
    return new Chart(ctx, config)
}