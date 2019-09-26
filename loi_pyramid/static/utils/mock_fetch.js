// Inspo from: (https://github.com/facebook/create-react-app/issues/967)
function mockFetch (ok, status, data) {
  return Promise.resolve({
    ok: ok,
    status: status,
    json: () => {
      return Promise.resolve(data)
    }
  })
}

export default mockFetch
