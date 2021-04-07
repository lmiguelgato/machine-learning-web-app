import React from 'react'
import Options from './options'

const CheckBox = (props) => {
    return (
        <>
            <Options
                optionDescription={props.optionDescription}
                isLoading={props.isLoading}
                option={props.option}
                setOption={props.setOption}/>
            { props.isLoading
                ? props.option.length
                ? props.option.length === 1 
                    ? <div>Training with option: { props.optionDescription[props.option[0][0]]}</div>
                    : <div>Training with options: { props.option.map((i) => {return props.optionDescription[i[0]]}) }</div>
                : null
                : null
            }
        </>
    );
}

export default CheckBox;