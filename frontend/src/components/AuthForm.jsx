import React from "react";
import style from "../style";
import ProfileData from "./ProfileData";
import TextField from "./TextField";
import { setLogin, setPassword } from "../reducer/authReducer";
import {useSelector} from "react-redux"

const AuthForm = ({profileName, processAuth}) => {
  const login = useSelector(state => state.login.value)
  const password = useSelector(state => state.password.value)

  const onSendClick = () => {
    processAuth(login, password)
  }

  return (
  <div style={style.mainBlock}>
    <ProfileData profileName={profileName}/>

    <div style={{...style.centered, ...style.mainForm}}>
      <h3 style={style.centeredWidth}>Авторизация</h3>

      <TextField label="Login" fieldStyle={style.logInDataField} actionCreator={setLogin}/>
      <TextField label="Password" type="password" fieldStyle={style.logInDataField} actionCreator={setPassword}/>

      <div style = {{...style.justifiedContent, ...style.centeredWidth}}>
          <button style={style.mainForm} onClick={onSendClick}>Отправить</button>
      </div>
    </div>
  </div>
  )
};

export default AuthForm;

