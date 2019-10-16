import tables from '../tables.js'

const mockOneRow = {
  mock: 1,
  sample: 'asdf'
}

const mockMultiRows = [{
  a: 1,
  b: 2
},
{
  a: 3,
  b: 4
}]

const mockMapRows = [{
  name: '1, 1',
  position: '1, 1'
},
{
  name: '0, 1',
  position: '0, 1'
},
{
  name: '2, 0',
  position: '2, 0'
}]

let mockAreas = mockMapRows.reduce((acc, area) => {
    return {...acc, [area.position]: {...area}}
  }, {})

document.body.innerHTML =
`<table id='oneRowTable'>
</table>
<table id='headerTable'>
    <thead>
        <tr>
            <th data-key="a"></th>
            <th data-key="b"></th>
        </tr>
    </thead>
</table>
<table id='mapTable'>
</table>`

const oneRowTable = document.querySelector('#oneRowTable')
const headerTable = document.querySelector('#headerTable')
const mapTable = document.querySelector('#mapTable')

beforeEach(() => {
  oneRowTable.innerHTML =
    `<tbody>
        <tr>
            <th data-key="mock"></th>
            <th data-key="sample"></th>
        </tr>
    </tbody>`

  if (headerTable.tBodies[0]) {
    headerTable.tBodies[0].innerHTML = ''
  }

  if (mapTable.tBodies[0]) {
    mapTable.tBodies[0].innerHTML = ''
  }
})

// maybe these should be integration tests
test('fillTableFromHeader()', () => {
  tables.fillTableFromHeader(headerTable, mockMultiRows)

  expect(headerTable.tBodies[0].rows.length).toBe(2)

  const headerRow = headerTable.tHead.children[0]
  for (let i = 0; i < headerTable.tBodies[0].children.length; i++) {
    const row = headerTable.tBodies[0].rows[i]
    for (let j = 0; j < row.children.length; j++) {
      const cell = row.children[j]
      const headerCell = headerRow.children[j]
      expect(cell.textContent).toBe(mockMultiRows[i][headerCell.dataset.key].toString())
    }
  }
})

// maybe these should be integration tests
test('fillOneRowFromHeader()', () => {
  tables.fillOneRowTable(oneRowTable, mockOneRow)

  expect(oneRowTable.rows.length).toBe(1)

  Array.from(oneRowTable.rows[0].children).forEach(cell => {
    expect(cell.textContent).toBe(mockOneRow[cell.dataset.key].toString())
  })
})

test('drawMap()', () => {

  tables.drawMap(mapTable, mockMapRows)

  //10 is the default
  expect(mapTable.tBodies[0].rows.length).toBe(10)

  for (let y = 0; y < mapTable.tBodies[0].children.length; y++) {
    const row = mapTable.tBodies[0].rows[y]

    //10 is the default
    expect(row.children.length).toBe(10)
    for (let x = 0; x < row.children.length; x++) {
      const cell = row.children[x]
      if (mockAreas[`${x},${y}`]) {
        expect(cell.textContent).toBe(mockAreas[`${x},${y}`].name)  
      } else {
        expect(cell.textContent).toBe('')
      }
    }
  }
})


test('drawMap() custom start end', () => {
  let startx = 1
  let starty = 0
  let endx = 2
  let endy = 2

  tables.drawMap(mapTable, mockMapRows, {startx: startx, endx: endx, endy: endy})

  expect(mapTable.tBodies[0].rows.length).toBe(endy - starty)

  for (let y = 0; y < mapTable.tBodies[0].children.length; y++) {
    const row = mapTable.tBodies[0].rows[y]

    expect(row.children.length).toBe(endx - startx)
    for (let x = 0; x < row.children.length; x++) {
      const cell = row.children[x]
      if (mockAreas[`${startx + x},${starty + y}`]) {
        expect(cell.textContent).toBe(mockAreas[`${startx + x},${starty + y}`].name)  
      } else {
        expect(cell.textContent).toBe('')
      }
    }
  }
})