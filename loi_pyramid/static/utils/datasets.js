export const dataset = (name, retrieve) => {
  const getData = (parentData) => {
    const data = sessionStorage.getItem(name)
    if (!data) {
      return retrieve(parentData)
        .then(data => {
          sessionStorage.setItem(name, JSON.stringify(data))
          return data
        })
        .catch(error => {
          throw new Error(error.message)
        })
    } else {
      return new Promise((resolve, reject) => {
        resolve(JSON.parse(data))
      })
    }
  }

  const clear = () => {
    sessionStorage.removeItem(name)
  }

  const attrs = () => {
    return {
      name: name,
      retrieve: retrieve
    }
  }

  return {
    getData: getData,
    clear: clear,
    attrs: attrs
  }
}
