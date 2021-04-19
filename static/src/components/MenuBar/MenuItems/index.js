import React from 'react'
import About from './about'
import ChangeRoute from './change-route'

const MenuItems = () => {
  return (
    <>
      {/* <ChangeRoute label='Webcam' link="/webcam"/> */}
      <ChangeRoute label='Rock/Paper/Scissors' link="/rock-paper-scissors"/>
      <About />
    </>
  )
}

export default MenuItems
