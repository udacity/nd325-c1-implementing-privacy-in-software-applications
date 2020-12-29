import React from 'react';
import { H5, FormGroup, InputGroup, RadioGroup, Radio, TextArea, Button, Intent, Toaster, IToaster } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";


export interface ICandidate {
  name: string
  candidate_id: string
}


interface IBallotFormState {
  candidates: ICandidate[]
  ballotNumber: string
  voterNationalId: string
  comments: string
  selectedCandidateId: string | undefined
}

const HOST_NAME = "127.0.0.1:5000";
const BASE_URL = "http://" + HOST_NAME + "/api";

const toaster: IToaster = Toaster.create();

export class IBallotForm extends React.PureComponent<{}, IBallotFormState> {

  state: IBallotFormState = {
    candidates: [],
    ballotNumber: "",
    voterNationalId: "",
    comments: "",
    selectedCandidateId: undefined
  };

  public componentDidMount() {
    fetch(BASE_URL + "/get_all_candidates")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            candidates: result as ICandidate[]
          });
        },
      )
  }

  public render() {
    const { ballotNumber, voterNationalId, comments, selectedCandidateId } = this.state;
    // TODO: Somewhere in the object returned below, we should be including language about voter secrecy, and a voter's right to deregister after voting to protect their data
    return (
    <>
      <FormGroup>
        <H5 className="white-text">Enter your voter information</H5>
        <InputGroup onChange={this.onNationalIdUpdate} value={voterNationalId} large={true} leftIcon={IconNames.PERSON} placeholder="Your National ID" />
        <br />
        <InputGroup onChange={this.onBallotNumberUpdate} value={ballotNumber} large={true} leftIcon={IconNames.DOCUMENT} placeholder="Your Ballot Number" />
        <br />
        <H5 className="white-text">Choose a Candidate for Chancellor of the Republic</H5>
        <RadioGroup selectedValue={this.state.selectedCandidateId} onChange={this.onCandidateSelect} inline={false}>
          {this.state.candidates.map(candidate =>
            <Radio key={candidate.candidate_id} label={candidate.name} value={String(candidate.candidate_id) as string} />
          )}
        </RadioGroup>
        <br />
        <H5 className="white-text">Additional Voter Comments</H5>
        <TextArea onChange={this.onCommentUpdate} growVertically={true} value={comments} fill={true} placeholder="Comments or concerns" />
      </FormGroup>
      <Button onClick={this.onVoteSubmission} intent={Intent.PRIMARY}>Submit Vote</Button>
    </>)
  }

  private onNationalIdUpdate = (event: React.FormEvent<HTMLInputElement>) => {
    this.setState({
      voterNationalId: event.currentTarget.value
    });
  }


  private onBallotNumberUpdate = (event: React.FormEvent<HTMLInputElement>) => {
    this.setState({
      ballotNumber: event.currentTarget.value
    });
  }


  private onCandidateSelect = (event: React.FormEvent<HTMLInputElement>) => {
    this.setState({
      selectedCandidateId: event.currentTarget.value
    });
  }

  private onCommentUpdate = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    this.setState({
      comments: event.currentTarget.value
    });
  }

  private onVoteSubmission = async (event: React.MouseEvent<HTMLElement>) => {
    const { ballotNumber, voterNationalId, comments, selectedCandidateId } = this.state;

    if (ballotNumber.length === 0) {
      toaster.show({
        message: "Please specify a ballot number",
        intent: Intent.DANGER
      });
      return;
    } else if (voterNationalId.length === 0) {
      toaster.show({
        message: "Please specify your National ID",
        intent: Intent.DANGER
      });
      return;
    } else if (selectedCandidateId === undefined) {
      toaster.show({
        message: "Please select a candidate",
        intent: Intent.DANGER
      });
      return;
    }

    const response = await fetch(BASE_URL + "/count_ballot", {
      method: 'POST',
      body: JSON.stringify({
        voter_national_id: voterNationalId,
        ballot_number: ballotNumber,
        chosen_candidate_id: selectedCandidateId,
        voter_comments: comments
      }),
      headers: {'Content-Type': 'application/json'}
    });

    // TODO: If the ballot was successfully counted, inform the user, and inform the user about deleting their voter details

    /* If we got a generic bad response, show a danger toast */
    if (!response.ok) {
      toaster.show({
        message: "There was a problem casting this ballot",
        intent: Intent.DANGER
      })
    } else {
      this.clearEnteredState();
    }
  }

  private clearEnteredState() {
    this.setState({
      ballotNumber: "",
      voterNationalId: "",
      comments: "",
      selectedCandidateId: undefined
    })
  }
}
