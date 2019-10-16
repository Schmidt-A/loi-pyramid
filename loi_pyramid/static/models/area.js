import { dataset } from '../utils/datasets.js'
import { BASE_URL } from '../environments/dev.js'

const areaData = dataset(
  'area',
  function () {
    let url = new URL(`${BASE_URL}/areas`)
    let params = {limit: 100, offset: 0}
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
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
})

export default areaData
