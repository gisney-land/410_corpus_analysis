import React, {Component} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import axios from "axios";
import { Graph } from 'react-d3-graph';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: "",
      data: null,
      nodes: [1, 2, 3],
      links: [[1, 2], [2, 3]],
    }
    this.handleOnChange = this.handleOnChange.bind(this);
    this.clearData = this.clearData.bind(this);
    this.confirmData = this.confirmData.bind(this);
    this.consoleData = this.consoleData.bind(this);
  }

  confirmData() {
    var self = this;
    axios.post("http://localhost:5000/api/confirmData", {
      text: self.state.text
    })
    .then(function (response) {
      self.setState({
        data: response.data.console,
        nodes: response.data.graph.nodes,
        links: response.data.graph.links

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
  }

  consoleData() {
    if (this.state.data === null) {
      return ""
    }
    else {
      return (
        this.state.data.map((entry, index) => {
          return <li key={index}>{entry}</li>
        })
      );
    }
  }

  graphData() {
    const nodes = this.state.nodes.map(node => {
      return {id: node}
    });
    const links = this.state.links.map(link => {
      return {source: link[0], target: link[1]}
    });
    const data = {
      nodes: nodes,
      links: links
    };
    const myConfig = {
      nodeHighlightBehavior: true,
      node: {
          color: 'lightgreen',
          size: 120,
          highlightStrokeColor: 'blue'
      },
      link: {
          highlightColor: 'lightblue'
      }
    };
   
  return <Graph
      id="graph-id" // id is mandatory, if no id is defined rd3g will throw an error
      data={data}
      config={myConfig}
  />;



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
              <Form.Label>Text Input</Form.Label>
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
            {
              this.graphData()
            }
          </div>
        </div>
        <div className="console">
          <h2>Console: </h2>
            {
              this.consoleData()
            }
        </div>
      </div>

    );
  }
}
