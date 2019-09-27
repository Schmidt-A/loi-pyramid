import mockFetch from '../../utils/mock_fetch.js'
import loginForm from '../login_form.js'
import noobAccount from '../../models/tests/__mocks__/noob_account.json'
import { BASE_URL } from '../../environments/dev.js'

beforeEach(() => {
  sessionStorage.clear()
})

// this is really about testing that forming of the POST
test('loginForm Listener eventFunction() success', () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return mockFetch(true, 200, {}) })

  const markup =
  `<form>
    <input type="text" name="user" value=mockUsername></input>
    <input type="password" name="pw" value="mockPassword"></input>
  </form>`
  document.body.innerHTML = markup

  const mockEvent = {
    srcElement: document.body.children[0],
    preventDefault: () => {}
  }

  loginForm.listeners[0].eventFunction(mockEvent)

  expect(window.fetch.mock.calls[0][0]).toBe(`${BASE_URL}/login`)
  expect(window.fetch.mock.calls[0][1].method).toBe('POST')

  const data = window.fetch.mock.calls[0][1].body
  expect(data.get('user')).toBe('mockUsername')
  expect(data.get('pw')).toBe('mockPassword')
})

// this is really about testing that forming of the POST
test('loginForm renderData() logout', () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return mockFetch(true, 200, {}) })

  sessionStorage.setItem('account', JSON.stringify(noobAccount))

  loginForm.renderData()

  expect(window.fetch.mock.calls[0][0]).toBe(`${BASE_URL}/logout`)

  expect(sessionStorage.getItem('account')).toBeNull()
})
