import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TestCaseList from './TestCaseList';
import UpdateTestCase from './UpdateTestCase';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/update/:id" element={<UpdateTestCase />} />
                <Route path="/" element={<TestCaseList />} />
            </Routes>
        </Router>
    );
};

export default App;
