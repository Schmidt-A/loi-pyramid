function fillTableFromHeader (table, dataList) {
  // that's the row within the thead
  const headerRow = table.tHead.children[0]

  if (!table.tBodies.length) {
    table.createTBody()
  }

  dataList.forEach(data => {
    const row = table.tBodies[0].insertRow()
    Array.from(headerRow.children).forEach(column => {
      const cell = row.insertCell()
      const text = document.createTextNode(data[column.dataset.key])
      cell.appendChild(text)
    })
  })
}

function fillOneRowTable (table, data) {
  // that's the row within the tbody
  const row = table.rows[0]

  Array.from(row.children).forEach(cell => {
    const text = document.createTextNode(data[cell.dataset.key])
    cell.appendChild(text)
  })
}

function drawMap (table, areas, { startx = 0, starty = 0, endx = 10, endy = 10} = {}) {
  let areaMap = areas.reduce((acc, area) => {
    return {...acc, [area.position]: {...area}}
  }, {})

  if (!table.tBodies.length) {
    table.createTBody()
  }

  for (let y = starty; y < endy; y++) {
    const row = table.tBodies[0].insertRow()
    for (let x = startx; x < endx; x++) {
      const cell = row.insertCell()

      if (areaMap[`${x},${y}`]) {
        const text = document.createTextNode(areaMap[`${x},${y}`].name)
        cell.appendChild(text)
      }
    }
  }
}

export default { fillTableFromHeader, fillOneRowTable, drawMap }
