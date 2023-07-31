

async function GetOrdersInfo(start, end){

    let response = await fetch(`/admin/api/AllOrders/?from=${start.toString()}&end=${end.toString()}`, {
        method:"GET",
        headers :{
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    let data = (await response).json()
    return data
}


window.addEventListener("DOMContentLoaded", async (e)=>{
    const today = moment().toISOString();
    const PreWeek = moment().subtract(1, 'week').toISOString();
    let response = await GetOrdersInfo(today, PreWeek)

    let xValues = []
    let yValues = []
    console.log(response)
    Array.from(response.data).forEach((value, index)=>{

        console.log(value)

    })


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