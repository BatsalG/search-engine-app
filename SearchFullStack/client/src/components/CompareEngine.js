import React from 'react'
import Results from './Results';
import { useState, useEffect } from 'react';
import './css/Compare.css';

const CompareEngine = ({ gres, bres }) => {
    return (
        <div className="entire">
            <div className="google_left">
                <div className="img_google">
                    <img src="https://www.freepnglogos.com/uploads/google-logo-png/file-google-logo-svg-wikimedia-commons-23.png" height="50" alt="file google logo svg wikimedia commons" />
                </div>
                {gres['0'].map(res => <Results res={res} group="doub_group" cols_num="double_result" />)}
            </div>

            <div className="bing_right">
                <div className="img_bing">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Bing_logo_%282016%29.svg/1280px-Bing_logo_%282016%29.svg.png" height="50" alt="file google logo svg wikimedia commons" />
                </div>
                {bres['0'].map(res => <Results res={res} group="doub_group" cols_num="double_result" />)}
            </div>
        </div>
    )
}

export default CompareEngine;