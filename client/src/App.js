import React, { useState, useEffect } from 'react'
import './App.css';

function App() {
  const [searchInput, setSearchInput] = useState("");
  const searchBar = () => {};
  const handleChange = (e) => {
      e.preventDefault();
      setSearchInput(e.target.value);
  };

  const logInput = () => {
      console.log(searchInput);
      postSearchInput();
  };

  const postSearchInput = () => {
      console.log("posting")
      fetch("/search", {
          method: "POST",
          body: JSON.stringify({
              search: searchInput
          }),
          headers: {
              "Content-type": "application/json; charset=UTF-8"
          }
      }).then(r => {
          console.log(r);
      })
  };

  return (
    <div className="App">
        <div className="SearchBar">
            <input type="text" name="search" placeholder="Search here" onChange={handleChange} value={searchInput} />
                <button className="search" onClick={() => logInput()}></button>
        </div>
    </div>
  );
}

export default App;

