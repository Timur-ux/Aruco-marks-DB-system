import React, { useEffect } from "react";
import style from "../style";
import DataField from "./DataField";
import { useState } from "react";
import processRequest from "../service/processRequest";
import { onFilled, setColumns, setRows } from "../reducer/table";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

const RequestListItem = ({ name, uri, type, fields }) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const states = fields.map((_) => "");

  const handleRequest = () => {
    navigate("/table_display");
  }

  const onClick = async () => {
    console.log("URI: ", uri);
    const namedParams = {}
    for (let i = 0; i < fields.length; i++) {
      namedParams[fields[i].name] = states[i]
    }

    console.log("Params: ", namedParams);
    const response = await processRequest(type, uri, namedParams)
    const data = response.data;
    if(data.type == "Tabled") {
      const {columns, rows} = data.data;
      dispatch(setColumns(columns));
      dispatch(setRows(rows));

      console.log("Clicked on: ", name);
      handleRequest();
    } else
      console.log("Warn: Tabled response type waited but given: ", data.type);
  };

  const fieldItems = [];
  for (let i = 0; i < fields.length; i++) {
    fieldItems.push(
      <DataField placeholder={fields[i].name} idx={i} states={states} />,
    );
  }

  return (
    <div>
      <button style={style.button} onClick={onClick}>
        {name}
      </button>
      <div style={{ ...style.justifiedContent, ...style.centeredWidth }}>
        {fieldItems}
      </div>
    </div>
  );
};

export default RequestListItem;
