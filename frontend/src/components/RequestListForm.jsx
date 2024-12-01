import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import style from "../style";
import RequestListItem from "./RequestListItem";

const RequestListForm = () => {
  const requests = useSelector((state) => state.requests.requests);
  const requestsItem = requests.map((request) => (
    <li>{<RequestListItem {...request}/>}</li>
  ));

  return (
    <ul style={{ ...style.mainForm, ...style.centered }}>{requestsItem}</ul>
  );
};

export default RequestListForm;
