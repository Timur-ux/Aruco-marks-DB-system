import "./App.css";
import style from "./style.js";
import StartForm from "./components/StartForm";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AuthForm from "./components/AuthForm";
import RequestListForm from "./components/RequestListForm";
import TableGenerator from "./components/TableGenerator";

const App = () => {
  return (
    <div style={style.mainBlock}>
      <Router>
        <div style={style.mainForm}>
          <Routes>
            <Route path="/" element={<StartForm />} />
            <Route path="/Auth" element={<AuthForm />} />
            <Route path="/requests" element={<RequestListForm />} />
            <Route path="/table_display" element={<TableGenerator />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
};

export default App;
