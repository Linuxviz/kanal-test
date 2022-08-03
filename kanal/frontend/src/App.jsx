import React, { Component } from 'react';
import { useState } from 'react';
import axios from 'axios';
import Graph from './Graph';

const baseURL = "http://0.0.0.0:8000/deals/"; //""/deals/"

function dtFormat (time) {
  let today = new Date(time);
  let day = today.getDate() + "";
  let month = (today.getMonth() + 1) + "";
  let year = today.getFullYear() + "";
  
  return checkZero(day) + "." + checkZero(month) + "." + year 
}

function checkZero(data){
  if(data.length == 1){
    data = "0" + data;
  }
  return data;
}

const App = () => {
  const [deals, Setposts] = useState([])

  React.useEffect(() => {
    axios.get(baseURL).then((response) => {
      Setposts(response.data.results);
    });
      setInterval(() => {
        console.log("biba"); 
        axios.get(baseURL).then((response) => {
          Setposts(response.data.results);
        })
      }, 60000);   
  }, []);


  return (
    <div className="App">
      <div>
        <table border="1">
        <tr>
        <th>№</th>
        <th>заказ №</th>
        <th>cтоимость, $</th>
        <th>cтоимость, руб</th>
        <th>срок поставки</th>
        </tr>
        {console.log(deals)}
        {deals.map((deal) => <tr><td>{deal.table_id}</td><td>{deal.order_id}</td><td>{deal.usa_dollar_price}</td><td>{deal.ruble_price}</td><td>{dtFormat(deal.delivery_time)}</td></tr>)}
        </table>
      <Graph items={deals}/>
      </div>
      
    </div>
  );
}

export default App;
