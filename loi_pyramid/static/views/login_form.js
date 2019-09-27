import Templates from '../utils/templates.js'
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

const loginForm = new Templates.Template(
  accountData,
  markup,
  function () {
    if (sessionStorage.getItem('account')) {
      sessionStorage.clear()
      return fetch(`${BASE_URL}/logout`)
    } else {
      return Promise.resolve()
    }
  },
  [new Templates.Listener(
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
    }
  )]
)
export default loginForm
