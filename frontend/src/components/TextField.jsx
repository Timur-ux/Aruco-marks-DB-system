import React  from "react";
import {useDispatch} from 'react-redux'

const TextField = ({label, blockStyle, fieldStyle, type, actionCreator}) => {
    const dispatch = useDispatch()
    const onTextChange = (e) => 
      dispatch(actionCreator(e.target.value));
    
    
    type = type ? type : "text";

  return (
    <div style={blockStyle}>
      <p>{label}</p>
      <input style={fieldStyle} type={type} onChange={onTextChange} onBlur={onTextChange}></input>
    </div>
  )
};

export default TextField;
