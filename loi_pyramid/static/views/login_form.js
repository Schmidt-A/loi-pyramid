import Templates from '../utils/templates.js'
import accountData from '../models/account.js'

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
      return fetch('http://sundred.com:6543/logout')
        .then(response => {
          sessionStorage.clear()
        })
        .catch(response => {})
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
      fetch('http://sundred.com:6543/login', {
        method: 'POST',
        body: formData
      })
        .then(response => {
          return response.json()
        })
        .then(account => {
          sessionStorage.setItem('account', JSON.stringify(account))
          window.dispatchEvent(new Event('triggerPage'))
        })
        .catch(error => {
          throw new Error(error)
        })
    }
  )]
)
export default loginForm
