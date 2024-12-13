import React from "react";
import style from "../style";

const ProfileData = ({profileName}) => (
  <div style={style.profileData}>Выбранный профиль: {profileName}</div>
);

export default ProfileData;
