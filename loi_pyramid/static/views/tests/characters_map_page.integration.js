import mockFetch from '../../utils/mock_fetch.js'
import charactersMapPage from '../characters_map_page.js'
import noobAccount from '../../models/tests/__mocks__/noob_account.json'
import noobCharacters from '../../models/tests/__mocks__/noob_characters.json'
import areas from '../../models/tests/__mocks__/areas.json'

const pageContainer = document.createElement('div')
pageContainer.id = 'pageContainer'
document.body.appendChild(pageContainer)

beforeEach(() => {
  sessionStorage.clear()
  sessionStorage.setItem('account', JSON.stringify(noobAccount))
  charactersMapPage.clear()
  expect(charactersMapPage.attrs().container).toBeFalsy()
})

const mockParse = url => {
  const list = url.pathname.split('/')
  const path = list[list.length - 1]
  if (path === 'characters') {
    return mockFetch(true, 200, noobCharacters)
  } else if (path === 'areas') {
    return mockFetch(true, 200, areas)
  } else {
    throw new Error(url)
  }
}

let areaMap = areas.areas.reduce((acc, area) => {
    return {...acc, [area.position]: {...area}}
  }, {})

test('Page render()', async () => {
  jest.spyOn(window, 'fetch').mockImplementation( (url) => { return mockParse(url) })

  await charactersMapPage.render(pageContainer)

  expect(window.location.pathname).toBe('/app/characters_map')

  const accountTable = charactersMapPage.attrs().contentMap.accountInfo.attrs().container.children[0]
  expect(accountTable).toBeInstanceOf(HTMLTableElement)
  expect(accountTable.rows.length).toBe(1)

  Array.from(accountTable.rows[0].children).forEach(cell => {
    expect(cell.textContent).toEqual(noobAccount[cell.dataset.key].toString())
  })

  const mapTable = charactersMapPage.attrs().contentMap.mapTable.attrs().container.children[0]
  expect(mapTable).toBeInstanceOf(HTMLTableElement)
  expect(mapTable.rows.length).toBe(11)

  for (let y = 0; y < mapTable.tBodies[0].children.length; y++) {
    const row = mapTable.tBodies[0].rows[y]
    expect(row.children.length).toBe(6)

    for (let x = 0; x < row.children.length; x++) {
      const cell = row.children[x]
      if (areaMap[`${x},${y}`]) {
        expect(cell.textContent).toBe(areaMap[`${x},${y}`].name)  
      } else {
        expect(cell.textContent).toBe('')
      }
    }
  }
})
