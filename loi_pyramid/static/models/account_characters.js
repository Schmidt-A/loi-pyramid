import { Dataset } from '../utils/datasets.js'
import { BASE_URL } from '../environments/dev.js'

const accountCharactersData = new Dataset(
  'accountCharacters',
  function (account) {
    if (account && account.username) {
      return fetch(`${BASE_URL}/accounts/${account.username}/characters`)
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error(JSON.stringify(response))
          }
        })
    } else {
      throw new TypeError('Account must be an object containing a username')
    }
  }
)

export default accountCharactersData
