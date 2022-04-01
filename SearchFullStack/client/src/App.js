import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';
import KeywordForm from './components/KeywordForm';
import Results from './components/Results';
import CompareEngine from './components/CompareEngine';
import ClipLoader from "react-spinners/ClipLoader";
import MainPart from './components/MainPart';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Analysis from './components/Analysis';
import Fetcher from './components/Fetcher'
import ActiveSchedule from './components/ActiveSchedule';
import { Navbar, Nav, Container } from 'react-bootstrap'
import './components/css/App.css';

function App() {
  const [kywd, setKey] = useState('');
  const [engine_name, setEngine] = useState('google');
  const [google_res, setGoogle] = useState([]);
  const [bing_res, setBing] = useState([]);
  const [loading, setLoading] = useState(false);

  const refreshResults = (kywd, engine_name) => {
    setLoading(true);
    setKey(kywd);
    const fetchAPI = '/results/' + kywd + '/' + engine_name.toLowerCase();
    setEngine(engine_name.toLowerCase());
    fetch(fetchAPI)
      .then(res => res.json())
      .then(data => {
        if (engine_name.toLowerCase() === 'google') {
          setGoogle(data['google']);
          setBing([]);
        } else if (engine_name.toLowerCase() === 'bing') {
          setBing(data['bing']);
          setGoogle([]);
        } else {
          setBing(data['bing']);
          setGoogle(data['google']);
        }
        setLoading(false)
      }
      );
  };
  const [value, setValue] = React.useState('one');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };


  return (

    <Router>

      <Navbar collapseOnSelect expand="lg"  style = {{ backgroundColor: '#14213d' }} variant = "dark">
        <Container>
          <Navbar.Brand href="#home">Internet Analysis</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="/">Fetch</Nav.Link>
              <Nav.Link href="/search">Search</Nav.Link>
              <Nav.Link href="/active">Active</Nav.Link>
            </Nav>
            <Nav>
              <Nav.Link href="/">About</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Routes>
        <Route path="/test" >

        </Route>
        <Route path="/search" element={<> <KeywordForm
          refreshResults={refreshResults}
          loader={loading}
        />
          <MainPart loading={loading} engine_name={engine_name} google_res={google_res} bing_res={bing_res} />
        </>} />

        <Route path="/analysis" element={<Analysis />} />
        <Route path="/" element={<Fetcher />} />
        <Route path="/active" element={<ActiveSchedule />} />

      </Routes>

      <div className="loader_circle">
        <ClipLoader color="red" loading={loading} size={150} />
      </div>
    </Router>
  );
}

export default App;