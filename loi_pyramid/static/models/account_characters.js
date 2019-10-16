import { dataset } from '../utils/datasets.js'
import { BASE_URL } from '../environments/dev.js'

const accountCharactersData = dataset(
  'accountCharacters',
  function (account) {
    // this username is problematic
    if (account && account.username) {
      let url = new URL(`${BASE_URL}/accounts/${account.username}/characters`)
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
      throw new TypeError('Account must be an object containing a username')
    }
  }
)

export default accountCharactersData
