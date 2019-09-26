import { Dataset } from '../utils/datasets.js'

const accountData = new Dataset(
  'account',
  function (username) {
    if (username) {
      return fetch(`http://sundred.com:6543/accounts/${username}`)
        .then(response => {
          if (response.ok) {
            return response.json()
          }
        })
        .catch(error => { throw new Error(error) })
    }
  }
)

export default accountData
