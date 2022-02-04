import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";

// component는 다른 components를 Render할 수 있다.
// App이라는 class는 우리의 첫번째 component인데,

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="center">
        <HomePage />
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
