import mockFetch from '../../utils/mock_fetch.js'
import loginPage from '../login_page.js'
import accountData from '../../models/account.js'
import noobAccount from '../../models/tests/__mocks__/noob_account.json'
import { BASE_URL } from '../../environments/dev.js'

const pageContainer = document.createElement('div')
pageContainer.id = 'pageContainer'
document.body.appendChild(pageContainer)

beforeEach(() => {
  accountData.clear()
  loginPage.clear()
  expect(loginPage.attrs().container).toBeFalsy()
})

test('Page render()', async () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return mockFetch(true, 200, noobAccount) })

  sessionStorage.setItem('account', 'mock')
  await loginPage.render(pageContainer)

  expect(window.fetch.mock.calls[0][0]).toBe(`${BASE_URL}/logout`)
  expect(sessionStorage.getItem('account')).toBeNull()

  expect(window.location.pathname).toBe('/app/login')

  // this indicates that these form fields have no value
  const form = document.querySelector('#login form')
  const user = document.querySelector("#login input[name='user']")
  const pw = document.querySelector("#login input[name='pw']")
  expect(user.value).toBeFalsy()
  expect(user.pw).toBeFalsy()

  user.value = noobAccount.username
  pw.value = 'drizzit4ever'
  form.dispatchEvent(new Event('submit', { bubbles: true }))

  expect(window.fetch.mock.calls[1][0].toString()).toBe(`${BASE_URL}/login`)
  expect(window.fetch.mock.calls[1][1].method).toBe('POST')

  const postData = window.fetch.mock.calls[1][1].body
  expect(postData.get('user')).toBe(noobAccount.username)
  expect(postData.get('pw')).toBe('drizzit4ever')

  expect(await accountData.getData(noobAccount.username)).toEqual(noobAccount)
  expect(sessionStorage.getItem('account')).toBe(JSON.stringify(noobAccount))
})
