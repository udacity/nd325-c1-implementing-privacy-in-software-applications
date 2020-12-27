import './App.css';
import React from 'react';
import { H1, H4 } from "@blueprintjs/core"
import { IBallotForm } from "./ballotForm"


function App() {
  return (
    <div className="app">
      <div className="app-header">
          <H1 className="white-text"> The Republic of Mars </H1>
          <H4 className="white-text"> DEPARTMENT OF ELECTORAL AFFAIRS </H4>
      </div>
      <div className="form">
        <IBallotForm />
        {/* <FormGroup>
            <H5 className="white-text">Enter your voter information</H5>
            <InputGroup large={true} leftIcon={IconNames.PERSON} placeholder="Your National ID" />
            <br />
            <InputGroup large={true} leftIcon={IconNames.DOCUMENT} placeholder="Your Ballot Number" />
            <br />
            <H5 className="white-text">Choose a Candidate for Chancellor of the Republic</H5>
            <RadioGroup inline={false}>
              <Radio label="Susan Schmidt" value="Susan Schmidt" />
              <Radio label="Martin Alvarez" value="Martin Alvarez" />
              <Radio label="Kimmy Ng" value="Kimmy Ng" />
            </RadioGroup>
            <br />
            <H5 className="white-text">Additional Voter Comments</H5>
            <TextArea fill={true} placeholder="Comments or concerns" />
        </FormGroup> */}
      </div>
    </div>
  );
}

export default App;
