import React from "react";
import AuthForm from "./AuthForm";
import { authFunc } from "../authFunc";
import { useSelector } from "react-redux";


const ProfileForm = ({access}) => {
  const stage = useSelector(state => state.stage.value)
  if(stage == "logging") {
    mainContent = <AuthForm profileName={access} processAuth={authFunc(access)}/>
  }
}
