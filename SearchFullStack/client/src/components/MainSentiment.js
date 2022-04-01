import React from 'react';
import { useState } from 'react';
import './css/MainSentiment.css';
import DocKey from './SentimentMain/DocKey';
import DocEmot from './SentimentMain/DocEmot';
import KeywordSent from './SentimentMain/KeywordSent';
import Entities from './SentimentMain/Entities';
import './css/Entities.css';
import ReactTooltip from "react-tooltip";

const MainSentiment = ({ doc_sentiment, kw_sentiment, keyword, text_char, document_emotions, kw_emotions, kw_list, entities }) => {
    return (
        <div>
            {console.log(entities)}
            <ReactTooltip id="textToolTip" place="top" effect="solid" multiline="true">
                Total number of characters in the article.
            </ReactTooltip>
            <ReactTooltip id="docTooltip" place="top" effect="solid" multiline="true">
                Overall sentiment of the document.
            </ReactTooltip>
            <ReactTooltip id="keyTooltip" place="top" effect="solid" multiline="true">
                Sentiment towards the keyword in the article.
            </ReactTooltip>
            <ReactTooltip id="docEmotTooltip" place="top" effect="solid" multiline="true">
                Categorize the emotion from the article.
            </ReactTooltip>
            <ReactTooltip id="kwTooltip" place="top" effect="solid" multiline="true">
                The top keywords from the article along with its relevance and sentiment.
            </ReactTooltip>
            <ReactTooltip id="entityTooltip" place="top" effect="solid" multiline="true">
                People, Places, Events, etc. from the article with its relevance and sentiment.
            </ReactTooltip>

            <div
                className="text_length"
            >
                Text Characters: <span> {text_char} </span>
                <span style={{ fontSize: "1.2em", cursor: "pointer" }} data-tip data-for="textToolTip"> ⓘ </span>
            </div>

            <DocKey
                doc_sentiment={doc_sentiment}
                kw_sentiment={kw_sentiment}
                keyword={keyword}
            />

            <DocEmot
                sad={document_emotions.sadness}
                joy={document_emotions.joy}
                fear={document_emotions.fear}
                disgust={document_emotions.disgust}
                anger={document_emotions.anger}
                txt="Document Emotion"
            />

            <DocEmot
                sad={kw_emotions.sadness}
                joy={kw_emotions.joy}
                fear={kw_emotions.fear}
                disgust={kw_emotions.disgust}
                anger={kw_emotions.anger}
                txt={keyword + " Emotion"}
            />
            <div className="breaker_title">
                Top Keywords, Relevance and Sentiment
                <span style={{ fontSize: "1.2em", cursor: "pointer" }} data-tip data-for="kwTooltip"> ⓘ </span>
            </div>
            <div className="entire_kw_analysis">
                <div className="breaker">
                    <div className="breaker_kw">
                        Keyword
                    </div>
                    <div className="breaker_rel">
                        Relevance
                    </div>
                    <div className="breaker_sent">
                        Sentiment
                    </div>
                </div>
                
                {
                    kw_list.map(kws =>
                        <KeywordSent
                            kw={kws.text}
                            sent={kws.sentiment.score}
                            relevance={kws.relevance}
                        />
                    )
                }

            </div>

            <div className="entities_title">
                Entities from the Article
                <span style={{ fontSize: "1.2em", cursor: "pointer" }} data-tip data-for="entityTooltip"> ⓘ </span>
            </div>

            <div className="entities">
                {
                    entities.map(kws =>
                        <Entities
                            type={kws.type}
                            text={kws.text}
                            sentiment={kws.sentiment.score}
                            relevance={kws.relevance}
                            confidence={kws.confidence}
                        />
                    )
                }
            </div>



        </div>
    )
}

export default MainSentiment;
