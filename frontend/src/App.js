import React, {Component} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import axios from "axios";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: ""
    }
    this.handleOnChange = this.handleOnChange.bind(this);
    this.clearData = this.clearData.bind(this);
    this.confirmData = this.confirmData.bind(this);
  }

  confirmData() {
    var self = this;
    axios.post("http://localhost:5000/api/confirmData", {
      text: self.state.text
    })
    .then(function (response) {
      self.setState({
        data: response.data
      });
      console.log(response.data)
    })
    .catch(function (error) {
      console.log(error);
    })
  };

  clearData() {
    this.setState({
      text: "",
    });
    console.log(this.state);
  }

  handleOnChange(event) {
    const name = event.target.name;
    const value = event.target.value;
    this.setState({
      [name]: value
    });
    console.log(this.state.text);
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-2">
            <li>
              <Button
                variant="primary"
                onClick={this.confirmData}
                block>
                Confirm
              </Button>
            </li>
            <li>
              <Button
                variant="primary"
                onClick={this.clearData}
                block>
                Clear
              </Button>
            </li>
            
          </div>
          <div className="col-md-5">
          <Form>
            <Form.Group controlId="input_text">
              <Form.Label>Example textarea</Form.Label>
              <Form.Control
                as="textarea" 
                rows="20" 
                className="noresize"
                onChange={this.handleOnChange}
                name="text"
                value={this.state.text} />
            </Form.Group>
          </Form>
          </div>
          <div className="col-md-5">
            One of three columns
          </div>
        </div>
        <div className="console">
          Console
        </div>
      </div>

    );
  }
}
