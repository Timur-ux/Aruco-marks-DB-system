import React from "react";
import { useSelector } from "react-redux";
import style from "../style";
import RequestListItem from "./RequestListItem";


const RequestListForm = () => {
  const requests = useSelector(state => state.requests).requests;
  console.log(requests)
  
  const requestsItem = requests.map(request => <li>{<RequestListItem label={request.label} uri={request.uri}/>}</li>)


  return (<ul style={{...style.mainForm, ...style.centered}}>{requestsItem}</ul>);
};

export default RequestListForm;
