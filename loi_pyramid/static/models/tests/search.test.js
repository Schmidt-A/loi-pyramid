import mockFetch from '../../utils/mock_fetch.js'
import { searchData } from '../search.js'
import noobAccount from './__mocks__/noob_account.json'
import { BASE_URL } from '../../environments/dev.js'

const mockParse = url => {
  const list = url.pathname.split('/')
  const username = list[list.length - 1]
  if (username === noobAccount.username) {
    return mockFetch(true, 200, noobAccount)
  } else {
    return mockFetch(false, 404, {})
  }
}

test('search', async () => {
  jest.spyOn(window, 'fetch').mockImplementation((url) => { return mockParse(url) })

  const request1 = searchData.getData('Xx')
    .then(data => {
      expect(data.username).toBe(noobAccount.username)
      return data
    })
    .catch(error => {
      console.log('request1 error')
      expect(error.message).toBe('{"ok":false,"status":404}')
      return error
    })

  const request2 = searchData.getData('XxDri')
    .then(data => {
      expect(data.username).toBe(noobAccount.username)
      return data
    })
    .catch(error => {
      console.log('request2 error')
      expect(error.message).toBe('{"ok":false,"status":404}')
      return error
    })

  const request3 = searchData.getData('XxDrizz')
    .then(data => {
      expect(data.username).toBe(noobAccount.username)
      return data
    })
    .catch(error => {
      console.log('request3 error')
      expect(error.message).toBe('{"ok":false,"status":404}')
      return error
    })

  const request4 = searchData.getData('XxDrizzit')
    .then(data => {
      expect(data.username).toBe(noobAccount.username)
      return data
    })
    .catch(error => {
      console.log('request4 error')
      expect(error.message).toBe('{"ok":false,"status":404}')
      return error
    })

  const request5 = searchData.getData('XxDrizzitxX')
    .then(data => {
      expect(data.username).toBe(noobAccount.username)
      return data
    })
    .catch(error => {
      console.log('request5 error')
      throw new Error(error.message)
    })

  await Promise.all([request1, request2, request3, request4, request5])
})
