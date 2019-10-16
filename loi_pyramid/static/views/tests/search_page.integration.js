import mockFetch from '../../utils/mock_fetch.js'
import { searchPage } from '../type_form.js'
import noobAccount from '../../models/tests/__mocks__/noob_account.json'
// figure out why the setup function isn't working
import waitForExpect from 'wait-for-expect'

const pageContainer = document.createElement('div')
pageContainer.id = 'pageContainer'
document.body.appendChild(pageContainer)

const mockParse = url => {
  const list = url.pathname.split('/')
  const username = list[list.length - 1]
  if (username === noobAccount.username) {
    return mockFetch(true, 200, noobAccount)
  } else {
    return mockFetch(false, 404, {})
  }
}

beforeEach(() => {
  sessionStorage.clear()
  searchPage.clear()
  expect(searchPage.attrs().container).toBeFalsy()
})

test('Page render()', async () => {
  jest.spyOn(window, 'fetch').mockImplementation((url) => { return mockParse(url) })

  await searchPage.render(pageContainer)

  expect(window.location.pathname).toBe('/app/search')
  expect(sessionStorage.getItem('account')).toBeNull()

  const user = document.querySelector('#search input')
  expect(user.value).toBeFalsy()

  user.value = noobAccount.username
  user.dispatchEvent(new Event('change', { bubbles: true }))

  await waitForExpect(() => {
    const accountTable = document.querySelector('#search table')
    expect(accountTable).toBeInstanceOf(HTMLTableElement)
    expect(accountTable.rows.length).toBe(1)

    //const printlist = []
    Array.from(accountTable.rows[0].children).forEach(cell => {
      //printlist.push(cell.textContent)
      expect(cell.textContent).toEqual(noobAccount[cell.dataset.key].toString())
    })
    //console.table(printlist)
  })
})
