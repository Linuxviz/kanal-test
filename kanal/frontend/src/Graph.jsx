import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";


export default function Graph({items}) {
  function checkZero(data){
    if(data.length == 1){
      data = "0" + data;
    }
    return data;
  }

  function dtFormat (time) {
    let today = new Date(time);
    let day = today.getDate() + "";
    let month = (today.getMonth() + 1) + "";
    let year = today.getFullYear() + "";
    
    return checkZero(day) + "." + checkZero(month) + "." + year 
  }

  let array = []

  function prepareArray (item) {
    let obj = {'time':dtFormat(item.delivery_time), 'total usa dollar price':item.usa_dollar_price}
    let flag = true
    for(let i in array) {
      if (array[i]['time'] == obj['time']) {
        flag = false
        array[i]['total usa dollar price'] = array[i]['total usa dollar price'] + obj['total usa dollar price']
      }
    }
    if (flag) {
      array.push(obj)
    }
   }
  
  items.sort(function(a,b){return new Date(a.delivery_time) - new Date(b.delivery_time);});
  items.map(prepareArray)
  
  return (
    <LineChart
      width={800}
      height={800}
      data={array}
      margin={{
        top: 30,
        right: 30,
        left: 30,
        bottom: 30
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis yAxisId="left" />
      <YAxis yAxisId="right" orientation="right" />
      <Tooltip />
      <Legend />
      <Line
        yAxisId="left"
        type="monotone"
        dataKey="total usa dollar price"
        stroke="#8884d8"
        activeDot={{ r: 20 }}
      />
    </LineChart>
  );
}
