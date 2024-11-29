import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import style from "../style";
import RequestListItem from "./RequestListItem";
import { dummy } from "../service/client";

const RequestListForm = () => {
  const requests = useSelector((state) => state.requests.requests);
  const requestsItem = requests.map((request) => (
    <li>{<RequestListItem {...request}/>}</li>
  ));

  // For update element when requests list will arrive
  useEffect(() => {}, dummy);

  return (
    <ul style={{ ...style.mainForm, ...style.centered }}>{requestsItem}</ul>
  );
};

export default RequestListForm;
