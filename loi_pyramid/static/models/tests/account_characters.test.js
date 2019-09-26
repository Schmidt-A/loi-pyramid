import mockFetch from '../../utils/mock_fetch.js'
import accountCharactersData from '../account_characters.js'
import noobAccount from './__mocks__/noob_account.json'
import noobCharacters from './__mocks__/noob_characters.json'

// these tests are kinda useless
test('accountCharacters retrieve()', async () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return mockFetch(true, 200, noobCharacters) })

  const characters = await accountCharactersData.retrieve(noobAccount)

  expect(characters).toBeTruthy()
  expect(characters).toBe(noobCharacters)
  expect(window.fetch.mock.calls[0][0]).toBe(`http://sundred.com:6543/accounts/${noobAccount.username}/characters`)
})
