import "./App.css";
import style from "./style.js";
import StartForm from "./startForm";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import UserPage from "./components/UserPage";
import AdminLogin from "./components/AdminLogin";
import RedactorLogin from "./components/RedactorLogin.jsx"

const App = () => {
  return (
    <div style={style.mainBlock}>
    <Router>
      <Routes>
        <Route path="/" element={<StartForm/>} />
        <Route path="/user" element={<UserPage />} />
        <Route path="/admin" element={<AdminLogin />} />
        <Route path="/redactor" element={<RedactorLogin />} />
      </Routes>
    </Router>
    </div>
  );
};

export default App;
