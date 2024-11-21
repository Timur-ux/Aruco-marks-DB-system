import React, { useState } from "react";

const TextField = ({label, blockStyle, fieldStyle, type}) => {
    const [text, setText] = useState("");
    const onTextChange = (e) => {
      setText(e.target.value);
    }
    
    type = type ? type : "text";
    
    const onTextBlur = (e) => {console.log(text);}

  return (
    <div style={blockStyle}>
      <p>{label}</p>
      <input style={fieldStyle} type={type} onChange={onTextChange} onBlur={onTextBlur}></input>
    </div>
  )
};

export default TextField;
