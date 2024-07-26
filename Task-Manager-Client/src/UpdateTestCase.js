import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const UpdateTestCase = () => {
  const { id } = useParams();
  const [testcase, setTestcase] = useState(null);
  const [status, setStatus] = useState("");

  useEffect(() => {
    // Fetch test case details on component mount
    axios
      .get(`http://127.0.0.1:5000/api/testcases/${id}`)
      .then((response) => {
        setTestcase(response.data);
        setStatus(response.data.status);
      })
      .catch((error) => {
        console.error("There was an error fetching the test case!", error);
      });
  }, [id]);

  const handleUpdate = () => {
    axios
      .put(`http://127.0.0.1:5000/api/testcases/${id}`, { status })
      .then((response) => {
        setTestcase((prevState) => ({
          ...prevState,
          status: status,
          last_updated: response.data.last_updated,
        }));
        console.log("Test case updated");
      })
      .catch((error) => {
        console.error("There was an error updating the test case!", error);
      });
  };

  if (!testcase) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h3>{testcase.test_case_name}</h3>
      <p>Last Updated: {testcase.last_updated}</p>
      <input
        type="text"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
        placeholder="Update Status"
      />
      <button onClick={handleUpdate}>Update Status</button>
    </div>
  );
};

export default UpdateTestCase;
