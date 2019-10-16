import { dataset } from '../utils/datasets.js'
import { BASE_URL } from '../environments/dev.js'

const accountData = dataset(
  'account',
  function (username) {
    // this username is problematic
    if (username) {
      let url = new URL(`${BASE_URL}/accounts/${username}`)
      return fetch(url)
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error(JSON.stringify(response))
          }
        })
        .catch(error => {
          throw new Error(error.message)
        })
    } else {
      throw new TypeError('Username must be a string')
    }
  }
)

export default accountData
