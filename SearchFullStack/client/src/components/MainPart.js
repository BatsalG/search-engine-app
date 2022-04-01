import React from 'react';
import CompareEngine from './CompareEngine';
import Results from './Results';
import { useState } from 'react';

const MainPart = ({ loading, bing_res, google_res, engine_name }) => {
    const [results, setResults] = useState([])
    const sendResData = (results) => {
        setResults(results);
    }
    return (
        <div>
            {loading ? "" : (
                engine_name === "google" ?
                    (google_res.map(res => (<Results res={res} cols_num="single_result" group='results_group' sendResData = {sendResData}/>))) :
                    engine_name === "bing" ?
                        (bing_res.map(res => (<Results res={res} cols_num="single_result" group='results_group' />))) :
                        (<CompareEngine gres={[google_res]} bres={[bing_res]} />))}
        </div>
    )
}

export default MainPart;
