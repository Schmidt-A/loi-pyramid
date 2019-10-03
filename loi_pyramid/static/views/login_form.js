import templates from '../utils/templates.js'
import accountData from '../models/account.js'
import { BASE_URL } from '../environments/dev.js'

const markup =
  `<form>
    <label for="user">Username</label> 
    <input type="text" name="user"></input>
    <label for="pw">Password</label>
    <input type="password" name="pw"></input>
    <input type="submit"></input>
  </form>`

const loginListener = templates.listener(
  'form',
  'submit',
  function (event) {
    event.preventDefault()
    const formData = new FormData(event.srcElement)
    fetch(`${BASE_URL}/login`, {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (response.ok) {
          return response.json()
        } else {
          throw new Error(JSON.stringify(response))
        }
      })
      .then(account => {
        sessionStorage.setItem('account', JSON.stringify(account))
        window.dispatchEvent(new Event('triggerPage'))
      })
      .catch(error => {
        throw new Error(error.message)
      })
  }
)

const logoutFunction = () => {
  if (sessionStorage.getItem('account')) {
    sessionStorage.clear()
    return fetch(`${BASE_URL}/logout`)
      .catch(error => {
        console.log(`logout: ${error.message}`)
      })
  } else {
    return Promise.resolve()
  }
}

const loginForm = {
  markup: markup,
  listeners: [loginListener],
  dataset: accountData,
  renderData: logoutFunction
}
export default loginForm
