import mockFetch from '../../utils/mock_fetch.js'
import accountCharactersPage from '../account_characters_page.js'
import noobAccount from '../../models/tests/__mocks__/noob_account.json'
import noobCharacters from '../../models/tests/__mocks__/noob_characters.json'

const pageContainer = document.createElement('div')
pageContainer.id = 'pageContainer'
document.body.appendChild(pageContainer)
accountCharactersPage.container = document.querySelector('#pageContainer')

beforeEach(() => {
  sessionStorage.clear()
  sessionStorage.setItem('account', JSON.stringify(noobAccount))
  accountCharactersPage.container.innerHTML = ''
  expect(accountCharactersPage.container.children.length).toBe(0)
})

test('Page render()', async () => {
  jest.spyOn(window, 'fetch').mockImplementation(() => { return mockFetch(true, 200, noobCharacters) })

  await accountCharactersPage.render()

  expect(window.location.pathname).toBe('/app/account_characters')

  const accountTable = accountCharactersPage.contentMap.accountInfo.container.children[0]
  expect(accountTable).toBeInstanceOf(HTMLTableElement)
  expect(accountTable.rows.length).toBe(1)

  Array.from(accountTable.rows[0].children).forEach(cell => {
    expect(cell.textContent).toEqual(noobAccount[cell.dataset.key].toString())
  })

  const characterTable = accountCharactersPage.contentMap.accountCharacters.container.children[0]
  expect(characterTable).toBeInstanceOf(HTMLTableElement)
  expect(characterTable.rows.length).toBe(3)

  const headerRow = characterTable.tHead.children[0]
  for (let i = 0; i < characterTable.tBodies[0].children.length; i++) {
    const row = characterTable.tBodies[0].rows[i]
    for (let j = 0; j < row.children.length; j++) {
      const cell = row.children[j]
      const headerCell = headerRow.children[j]
      expect(cell.textContent).toEqual(noobCharacters.characters[i][headerCell.dataset.key].toString())
    }
  }
})
