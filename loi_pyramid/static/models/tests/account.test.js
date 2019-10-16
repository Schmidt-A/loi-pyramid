import mockFetch from '../../utils/mock_fetch.js'
import accountData from '../account.js'
import noobAccount from './__mocks__/noob_account.json'
import { BASE_URL } from '../../environments/dev.js'

// these tests are kinda useless
test('account retrieve()', async () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return mockFetch(true, 200, noobAccount) })

  const account = await accountData.attrs().retrieve(noobAccount.username)

  expect(account).toBeTruthy()
  expect(account).toBe(noobAccount)
  expect(window.fetch.mock.calls[0][0].toString()).toBe(`${BASE_URL}/accounts/${noobAccount.username}`)
})

test('account retrieve() bad input', () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return Promise.resolve(Response.error()) })

  expect(() => { accountData.retrieve() }).toThrow()

  expect(window.fetch).not.toHaveBeenCalled()
})
