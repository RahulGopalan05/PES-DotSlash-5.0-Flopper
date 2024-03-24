import React, { useEffect, useState } from 'react';

function NewPage() {
  const [data, setData] = useState('');

  useEffect(() => {
    // Fetch data from the backend when the component is mounted
    fetch('http://localhost:5000/newPage')
      .then(response => response.text())
      .then(data => setData(data));
  }, []);

  const startScript1 = () => {
    fetch('http://localhost:5000/start_script1');
  };

  const startScript2 = () => {
    fetch('http://localhost:5000/start_script2');
  };

  return (
    <div>
      <h2>{data}</h2>
      <button onClick={startScript1}>Start Script 1</button>
      <button onClick={startScript2}>Start Script 2</button>
    </div>
  );
}

export default NewPage;