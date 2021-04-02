import React, { useState } from 'react'
import MLCamera from '../../components/MLCamera/index'


const RockPaperScissors = (props) => {
    return (
        <>
            <MLCamera
                screenshotFormat="image/jpeg"
                height="200px"
                endpoint={props.endpoint + 'capture'}/>
            { props.children }
        </>
    );
}

export default RockPaperScissors;