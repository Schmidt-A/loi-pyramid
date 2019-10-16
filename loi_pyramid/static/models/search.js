import { BASE_URL } from '../environments/dev.js'

const newDataset = (retrieve) => {
  let latest
  let current

  const getData = (parentData) => {
    if (current) {
      latest = parentData
    } else {
      const data = retrieve(parentData)
        .then(data => {
          current = null
          if (latest === parentData) {
            return data
          } else {
            return getData(latest)
              .then(data => {
                return data
              })
              .catch(error => {
                throw new Error(error.message)
              })
          }
        })
        .catch(error => {
          current = null
          if (latest === parentData) {
            throw new Error(error.message)
          } else {
            return getData(latest)
              .then(data => {
                return data
              })
              .catch(error => {
                throw new Error(error.message)
              })
          }
        })

      latest = parentData
      if (!current) {
        current = data
      }
    }

    return current
  }

  const attrs = () => {
    return {
      name: name,
      retrieve: retrieve
    }
  }

  return {
    getData: getData,
    attrs: attrs
  }
}

export const searchData = newDataset(
  function (username) {
    // this username is problematic
    if (username) {
      return fetch(`${BASE_URL}/accounts/${username}`)
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
