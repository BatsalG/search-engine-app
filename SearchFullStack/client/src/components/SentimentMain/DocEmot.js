import React from 'react';
import '../css/MainSentiment.css';
import ReactTooltip from "react-tooltip";

const DocEmot = ({ sad, joy, fear, anger, disgust, txt }) => {
    return (
        <div>
            <div className="txt">
                {txt}
                <span style={{ fontSize: "1.2em", cursor: "pointer" }} data-tip data-for="docEmotTooltip"> ⓘ </span>

            </div>
            <div className="emot_container">
                <div className="doc_emot">
                    <div className="ind_emot">
                        <div className="joy">
                            <img src="https://cdn.shopify.com/s/files/1/1061/1924/products/Emoji_Icon_-_Smiling_large.png?v=1571606089" alt="" width="30px" />
                            <br />
                            Joy
                        </div>
                        <div className="emot_val">
                            {joy}
                        </div>
                    </div>

                    <div className="ind_emot">
                        <div className="sadness">
                            <img src="https://cdn.shopify.com/s/files/1/1061/1924/products/Sad_Face_Emoji_large.png?v=1571606037" alt="" width="30px" />
                            <br />
                            Sadness
                        </div>
                        <div className="emot_val">
                            {sad}
                        </div>
                    </div>
                    <div className="ind_emot">
                        <div className="fear">
                            <img src="https://cdn.shopify.com/s/files/1/1061/1924/products/Fearful_Face_Emoji_large.png?v=1571606037" alt="" width="30px" />
                            <br />
                            Fear
                        </div>
                        <div className="emot_val">
                            {fear}
                        </div>
                    </div>
                    <div className="ind_emot">
                        <div className="anger">
                            <img src="http://cdn.shopify.com/s/files/1/1061/1924/products/Super_Angry_Face_Emoji_ios10_grande.png?v=1571606092" alt="" width="30px" />
                            <br />
                            Anger
                        </div>
                        <div className="emot_val">
                            {anger}
                        </div>
                    </div>
                    <div className="ind_emot">
                        <div className="disgust">
                            <img src="https://emojis.wiki/emoji-pics/apple/nauseated-face-apple.png" alt="" width="30px" />
                            <br />
                            Disgust
                        </div>
                        <div className="emot_val">
                            {disgust}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default DocEmot;