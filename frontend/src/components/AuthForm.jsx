import React from "react";
import style from "../style";
import ProfileData from "./ProfileData";
import TextField from "./TextField";
import { setLogin, setPassword, setAccess } from "../reducer/authReducer";
import { useDispatch, useSelector } from "react-redux";
import { useLocation, useParams } from "react-router";
import { authFunc } from "../service/authFunc";
import { useNavigate } from "react-router";
import fetchRequests from "../service/fetchRequests";
import { dummy } from "../service/client";
import { setRequests } from "../reducer/requests";

const AuthForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const profileName  = useSelector(state => state.profile.name);
  const { access } = useParams();

  const processAuth = authFunc(access);

  const login = useSelector((state) => state.login.value);
  const password = useSelector((state) => state.password.value);

  const onSendClick = () => {
    console.log("Processing auth...");

    processAuth(login, password).then((response) => {
      console.log("Status: ", response.status, response.statusText);

      if (response.status == 200) {
        dispatch(setAccess(access));

        fetchRequests(access).then((responseData) => {
          const requests = responseData.data.requests;
          dispatch(setRequests({ requests: requests }));

          navigate("/profile/requests");
        });
      } else {
        console.log("Invalid auth", response);
      }
    });
  };

  return (
    <div style={{ ...style.centered }}>
      <h3 style={style.textCentered}>Авторизация</h3>

      <TextField
        label="Login"
        fieldStyle={style.logInDataField}
        actionCreator={setLogin}
      />
      <TextField
        label="Password"
        type="password"
        fieldStyle={style.logInDataField}
        actionCreator={setPassword}
      />

      <div style={{ ...style.justifiedContent, ...style.centered }}>
        <button
          style={{ ...style.button, ...style.centered }}
          onClick={onSendClick}
        >
          Отправить
        </button>
      </div>
    </div>
  );
};

export default AuthForm;
