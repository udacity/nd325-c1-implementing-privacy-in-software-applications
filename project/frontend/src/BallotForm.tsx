import React from 'react';


export interface ICandidate {
  name: string
  candidateId: string
}


interface IBallotFormState {
  candidates: ICandidate[]
}

const HOST_NAME = "127.0.0.1:5000";
const BASE_URL = "http://" + HOST_NAME + "/api/";

export class IBallotForm extends React.PureComponent<{}, IBallotFormState> {

  state: IBallotFormState = {
    candidates: []
  };

  public componentDidMount() {
    fetch(BASE_URL + "get_all_candidates")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            candidates: result as ICandidate[]
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  public render() {
    const { error, isLoaded, items } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              {item.name} {item.price}
            </li>
          ))}
        </ul>
      );
    }
  }
  }