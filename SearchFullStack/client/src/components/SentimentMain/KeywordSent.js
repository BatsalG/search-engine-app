import React from 'react';
import '../css/KeywordSent.css';

const KeywordSent = ({ kw, sent, relevance }) => {
    return (
        <div className = "cols_kw">
            <div className="kw_">
                {kw}
            </div>
            <div className="relevance_">
                {relevance}
            </div>
            <div className="sent_">
                {sent}
            </div>
            


        </div>
    )
}

export default KeywordSent;