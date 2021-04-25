import React from "react";
import ReactDOM from "react-dom";
import "./styles.css";

class App extends React.Component {
  state = {
    result: "",
    bust: "",
    waist: "",
    hip: "",
    bodyshape: ""
  };
  calBmi = () => {
    const { bust, waist, hip } = this.state;
    console.log(bust);

    const high = Math.max(bust, waist, hip)
    const low = Math.min(bust, waist, hip)
    const difference = high - low

    if( hip==="" && bust==="" && waist==="") {
      this.setState({
        bodyshape: "give correct inputs"
      });
    }
else{
     if (Number(waist) * 1.25 <= bust & hip) {
      this.setState({
        bodyshape: "Hourglass"
      });
    }
    else if (Number(hip) * 1.05 > bust) {
      this.setState({
        bodyshape: "Pear"
      });
    }
    else if (Number(hip) * 1.05 < bust) {
      this.setState({
        bodyshape: "Apple"
      });
    }
    if (difference<=5) {
      this.setState({
        bodyshape: "Rectangle"
      });
    }
  }



  };
  clearAll = () => {
    console.log("test");
    this.setState({
      height: "",
      weight: "",
      bust: "",
      waist: "",
      hip: "",
      result: "", 
      bodyshape:""
    });
  };

  render() {
    return (
      <div className="App">
        <div className="container">
         
          <div className="ui card">
            <div className="field">
              <div className="two fields">
                
                <div className="field">
                  <label>Bust: </label>
                  <br/>

                  <input
                    type="number"
                    placeholder="Bust size in inches"
                    value={this.state.bust}
                    onChange={e => this.setState({ bust: e.target.value })}
                  />
                </div>

                <br />
                <div className="field">
                  <label>Waist: </label>
                  <br/>

                  <input
                    type="number"
                    placeholder="Waist in inches"
                    value={this.state.waist}
                    onChange={e => this.setState({ waist: e.target.value })}
                  />
                </div>

                <br />
                <div className="field">
                  <label>Hip: </label>
                  <br/>

                  <input
                    type="number"
                    placeholder="Hip in inches"
                    value={this.state.hip}
                    onChange={e => this.setState({ hip: e.target.value })}
                  />
                </div>


              </div>
              <button className="ui button check" onClick={this.calBmi}>
                Check
              </button>
              <button
                className="ui button"
                onClick={this.clearAll}
              >
                Clear
              </button>
            </div>
           <h3> <p className="bmi-display">{` Your Body shape is`} <br/> <h2>{`${this.state.bodyshape} `} </h2> </p> </h3>
            <p className="result-display">{this.state.result}</p>
          </div>
        </div>
      </div>
    );
  }
}

export default App

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
