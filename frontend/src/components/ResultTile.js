import React, { Component } from "react";

export default class ResultTile extends Component {

  render() {
    const { row } = this.props;
    const {tile_images} = this.props;
    return (
      <div className="main">
          <div className="heading">
             <div className="title">
                 {row.title}
             </div>
          </div>

          <div className="body_tile container row ">
            <div className="col">
                <img className="image"
                     src={tile_images[row.category]}
                     alt="Not found"
                />
            </div>
            <div className="col">
              <div> Height : {(row.size.height/100).toFixed(2)} m </div>
              <div> Width  : {(row.size.width/100).toFixed(2)} m </div>
              <div> length : {(row.size.length/100).toFixed(2)} m </div>
              <div> Weight : {(row.weight/1000).toFixed(2)} kg </div>

            </div>
          </div>
          <div className="row result">
            <div> Average Cubic Weight = { ((row.size.height/100) *
                                           (row.size.width / 100) *
                                           (row.size.length/100) * 250).toFixed(2)} kg</div>
          </div>


      </div>
    );
  }
}
