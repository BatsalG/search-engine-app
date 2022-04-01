import React from 'react';
import '../css/MainSentiment.css';
import { useState, useEffect } from 'react';
import ReactTooltip from "react-tooltip";

const DocKey = ({ doc_sentiment, kw_sentiment, keyword }) => {
    const smiley = "https://www.pngmart.com/files/15/Happy-Face-PNG-Free-Download.png";
    const sad = "https://image.pngaaa.com/507/71507-middle.png";


    return (
        <div>
            <div className="container">
                <div className="doc_sentiment">
                    <div className="doc_1">
                        Document Sentiment
                        <span style={{ fontSize: "1.2em", cursor: "pointer" }} data-tip data-for="docTooltip"> ⓘ </span>

                    </div>
                    <div className="sent">
                        {doc_sentiment > 0 ? <img src={smiley} alt="" width="30px" /> : <img src={sad} alt="" width="30px" />}

                        &nbsp;&nbsp;
                        {doc_sentiment}
                    </div>
                </div>

                <div className="kw_sentiment">
                    <div className="doc_1">
                        Sentiment for <span> {keyword} </span>
                        <span style={{ fontSize: "1.2em", cursor: "pointer" }} data-tip data-for="keyTooltip"> ⓘ </span>
                    </div>
                    <div className="sent">
                        {kw_sentiment > 0 ? <img src={smiley} alt="" width="30px" /> : <img src={sad} alt="" width="30px" />}
                        &nbsp;&nbsp;
                        {kw_sentiment}
                    </div>
                </div>
            </div>

        </div>
    )
}

export default DocKey;
