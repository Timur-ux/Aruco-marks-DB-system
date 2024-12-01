import React from "react";
import { Outlet} from "react-router-dom";
import ProfileData from "./ProfileData";
import { useSelector } from "react-redux";

const Profile = () => {
  const profileName  = useSelector(state => state.profile.name);

  return (
    <div>
      <ProfileData profileName={profileName} />
      <Outlet />
    </div>
  );
};

export default Profile;
