import './App.css';
import { H1, H4, H5, FormGroup, InputGroup, RadioGroup, Radio } from "@blueprintjs/core"
import { IconNames } from "@blueprintjs/icons"

function App() {
  return (
    <div className="app">
      <div className="app-header">
          <H1> REPUBLIC OF MARS </H1>
          <H4> Election of the Chancellor of the Republic </H4>
      </div>
      <div className="form">
        <FormGroup>
            <H5>Enter your voter information</H5>
            <InputGroup large={true} leftIcon={IconNames.PERSON} placeholder="Your National ID" />
            <br />
            <InputGroup large={true} leftIcon={IconNames.DOCUMENT} placeholder="Your Ballot Number" />
            <br />
            <H5>Choose a Candidate for Chancellor of the Republic</H5>
            <RadioGroup inline={false}>
              <Radio label="Susan Schmidt" value="Susan Schmidt" />
              <Radio label="Martin Alvarez" value="Martin Alvarez" />
              <Radio label="Kimmy Ng" value="Kimmy Ng" />
            </RadioGroup>
        </FormGroup>
      </div>
    </div>
  );
}

export default App;
