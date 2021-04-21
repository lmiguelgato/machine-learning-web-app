import React from 'react'
import { Navbar, NavbarBrand } from 'reactstrap'
import MenuItems from './MenuItems'

const Bar = (props) => {
  return (
      <>
        <Navbar dark color="primary">
          <div className="container">
            <NavbarBrand href="/">
                {props.title}
            </NavbarBrand>

            <MenuItems/>
          </div>
        </Navbar>
      </>
  )
}

export default Bar
