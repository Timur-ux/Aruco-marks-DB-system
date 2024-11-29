import React from "react";
import style from "../style";
import DataField from "./DataField";
import { useState } from "react";
import processRequest from "../service/processRequest";

const RequestListItem = ({ name, uri, type, fields }) => {
  const states = fields.map((_) => "");

  const onClick = () => {
    console.log("URI: ", uri);
    const namedParams = {}
    for (let i = 0; i < fields.length; i++) {
      namedParams[fields[i].name] = states[i]
    }

    console.log("Params: ", namedParams);
    const response = processRequest(type, uri, namedParams)
    console.log("Response: ", response)
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
