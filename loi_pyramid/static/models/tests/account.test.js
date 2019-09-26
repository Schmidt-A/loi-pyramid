import mockFetch from '../../utils/mock_fetch.js'
import accountData from '../account.js'
import noobAccount from './__mocks__/noob_account.json'

// these tests are kinda useless
test('account retrieve()', async () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return mockFetch(true, 200, noobAccount) })

  const account = await accountData.retrieve(noobAccount.username)

  expect(account).toBeTruthy()
  expect(account).toBe(noobAccount)
  expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noobAccount.username}`)
})

test('account retrieve() bad input', () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return Promise.resolve(Response.error()) })

  expect( () => { accountData.retrieve() }).toThrow()
  
  expect(window.fetch).not.toHaveBeenCalled()
})