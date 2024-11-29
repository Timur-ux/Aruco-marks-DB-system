import React from "react";
import style from "../style";
import ProfileData from "./ProfileData";
import TextField from "./TextField";
import { setLogin, setPassword, setAccess } from "../reducer/authReducer";
import {useDispatch, useSelector} from "react-redux"
import { useLocation } from "react-router";
import { authFunc } from "../service/authFunc";
import { useNavigate } from "react-router";
import fetchRequests from "../service/fetchRequests";
import { dummy } from "../service/client";
import { setRequests } from "../reducer/requests";

const AuthForm = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const {profileName, access} = useLocation().state
  const processAuth = authFunc(access)

  const login = useSelector(state => state.login.value)
  const password = useSelector(state => state.password.value)

  const onSendClick = () => {
    console.log("Processing auth...")

    processAuth(login, password).then((response) => {
      console.log("Status: ", response.status, response.statusText)

      if(response.status == 200) {
        dispatch(setAccess(access))

        fetchRequests(access).then((data) => {
          const requests = data.data;
          dispatch(setRequests({ requests: requests }));
          dummy();
        });

        navigate("/requests")
      }
      else {
        console.log("Invalid auth", response);
      }
    })
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

