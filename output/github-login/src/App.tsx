import { useState } from 'react'
import LoginForm from './components/LoginForm'
import Footer from './components/Footer'
import './App.css'

function App() {
  return (
    <div className="page">
      <main className="login-container">
        <LoginForm />
      </main>
      <Footer />
    </div>
  )
}

export default App
