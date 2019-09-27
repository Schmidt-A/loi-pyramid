import { Dataset } from '../utils/datasets.js'
import { BASE_URL } from '../environments/dev.js'

const accountData = new Dataset(
  'account',
  function (username) {
    if (username) {
      return fetch(`${BASE_URL}/accounts/${username}`)
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error(JSON.stringify(response))
          }
        })
    } else {
      throw new TypeError('Username must be a string')
    }
  }
)

export default accountData
