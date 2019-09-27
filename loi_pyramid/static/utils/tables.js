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

export default { fillTableFromHeader, fillOneRowTable }
