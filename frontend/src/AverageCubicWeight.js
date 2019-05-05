import React, { Component } from "react";
import Select from 'react-select';
import axios from "axios";
import ResultTile from "./components/ResultTile";


const options = [
  { value: 'Airconditioners', label: 'Air Conditioners' },
  { value: 'Batteries', label: 'Batteries' },
  { value: 'Gadgets', label: 'Gadgets'},
  { value: 'Cabel', label:'Cables & Adapters'},
  { value: 'Food', label:'Food Preparation'},
  { value: 'Automotive', label:'Automotive Accessories'} ,
];

const tile_images = {
  'Air Conditioners': "https://azcd.harveynorman.com.au/media/catalog/product/cache/21/image/992x558/9df78eab33525d08d6e5fb8d27136e95/q/_/q_series_indoor_head_unit_2.5kw.jpg",
  'Batteries': "http://pngimg.com/uploads/automotive_battery/automotive_battery_PNG12111.png",
  'Gadgets':"https://images.pexels.com/photos/325153/pexels-photo-325153.jpeg",
  'Cables & Adapters':"https://ae01.alicdn.com/kf/HTB1UwscRFXXXXaqXVXXq6xXFXXXo/High-Quality-6mm-10awg-Solar-Cable-PV-Cabel-With-TUV-UL-Approval-10m-roll.jpg_640x640.jpg",
  'Food Preparation':"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXL20oXkvvmiSSJlDTOgam2ukdqsdxEuLqnEcBvQelP2DxB0yWlQ",
  'Automotive Accessories': "https://csninc.ca/wp-content/uploads/2014/05/auto-accessories.jpg"
};

const base_url = 'http://localhost:8000';

export default class AverageCubicWeight extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedOption: options.filter(option => option.value === 'Airconditioners')[0],
      avg_cubic_weight: 0,
      result_list: []
    };
  }

  componentDidMount() {
      this.handleChange(this.state.selectedOption);
  };

  render_result = () => {
    return (
      <div>
          {this.state.avg_cubic_weight > 0 &&
            <div>
              <br/>
              <h5 className="result">
                  <bold> Average cubic weight = {this.state.avg_cubic_weight.toFixed(2)} kg
                  </bold>
              </h5>
            </div>
          }
      </div>
    );
  };

  refreshList = (res) => {
    this.setState({
                  avg_cubic_weight: res.data.avg_cubic_weight,
                  result_list : res.data.result_list
                  });
  };

  handleChange = (selectedOption) => {
    this.setState({ selectedOption });
    axios
        .get(base_url +`/kogan/category/${selectedOption.label}/average_cubic_weight/`)
        .then(res => this.refreshList(res))
        .catch(err => console.log(err));

  };

  render() {

    return (
      <main className="content">
        <h1 className="text-center">
            <img className="logo_image"
             src="https://images.pexels.com/photos/19677/pexels-photo.jpg?auto=compress&cs=tinysrgb&dpr=1&w=500"
             alt="Not found"
            />
            Average cubic weight app
        </h1>
        <br/>
        <div className="row ">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <Select
              value={this.state.selectedOption}
              onChange={this.handleChange}
              options={options}

            />
          </div>
        </div>
         <div className="row ">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
              {this.render_result()}
          </div>
         </div>
          <div className="row">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="tiles">
                {this.state.result_list && this.state.result_list.map((row, index) => (
                    <ResultTile row={row} key={index} tile_images={tile_images} />
                  ))
                }
            </div>
          </div>
         </div>
      </main>
    );
  }
}
