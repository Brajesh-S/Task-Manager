import React, { useEffect, useState } from "react";
import axios from "axios";
import "./TestCaseList.css";

const TestCaseList = () => {
  const [testCases, setTestCases] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/testcases")
      .then((response) => response.json())
      .then((data) => {
        // Sort test cases by ID in ascending order
        const sortedTestCases = data.sort((a, b) => a.id - b.id);
        setTestCases(sortedTestCases);
      })
      .catch((error) => console.error("Error fetching test cases:", error));
  }, []);

  const handleStatusChange = (id, newStatus) => {
    axios
      .put(`http://127.0.0.1:5000/api/testcases/${id}`, { status: newStatus })
      .then((response) => {
        // Update the local state with the new status and last updated time
        setTestCases((prevTestCases) =>
          prevTestCases.map((testCase) =>
            testCase.id === id
              ? {
                  ...testCase,
                  status: newStatus,
                  last_updated: response.data.last_updated,
                }
              : testCase
          )
        );
      })
      .catch((error) =>
        console.error("There was an error updating the test case!", error)
      );
  };

  return (
    <div className="page-container">
      <div className="test-case-list">
        <div className="header">
          <div className="header-line"></div>
        </div>
        <div className="search-container">
          <input
            type="text"
            placeholder="Search issue.."
            className="search-input"
          />
          <button className="search-button">🔍</button>
        </div>
        <div className="table-container">
          <div className="filter-container">
            <button className="filter-button">Filter ▼</button>
          </div>
          <table>
            <thead>
              <tr>
                <th>Test Case Name</th>
                <th>Estimate Time</th>
                <th>Module</th>
                <th>Priority</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {testCases.map((testCase) => (
                <tr key={testCase.id}>
                  <td>
                    <div>Test Case ID: {testCase.id}</div>
                    <div className="last-updated">
                      Last Updated: {testCase.last_updated}
                    </div>
                  </td>
                  <td>{testCase.estimate_time}</td>
                  <td>{testCase.module}</td>
                  <td>{testCase.priority}</td>
                  <td>
                    <select
                      value={testCase.status}
                      onChange={(e) =>
                        handleStatusChange(testCase.id, e.target.value)
                      }
                    >
                      <option value="Select" disabled>
                        Select
                      </option>
                      <option value="PASS">PASS</option>
                      <option value="FAIL">FAIL</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TestCaseList;
