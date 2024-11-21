import React, { useState } from "react";
import style from "../style";
import ProfileData from "./ProfileData";

const AdminLogin = () => {
  const [ login, setLogin] = useState("");
  const [ password, setPassword] = useState("");

  const onLoginChange = (event) => {
    setLogin(event.target.value);
  }

  const onPasswordChange = (event) => 
    setPassword(event.target.value);

  const onLoginBlur = () => {
    console.log("Inputted login: ", login);
  }
  
  const onPasswordBlur = () => {
    console.log("Inputted password: ", password);
  }

  return (
  <div style={style.mainBlock}>
    <ProfileData profileName="Администратор"/>
    <div style={{...style.centered, ...style.mainForm}}>
      <p><h3>Авторизация</h3></p>
      <input style={style.logInDataField} type="text" onChange={onLoginChange} onBlur={onLoginBlur}></input>
      <input style={style.logInDataField} type="text" onChange={onPasswordChange} onBlur={onPasswordBlur}></input>
    </div>
  </div>
  )
};

export default AdminLogin;
