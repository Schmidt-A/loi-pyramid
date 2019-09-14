function fillTableFromHeader(table, dataList) {
    //that's the row within the thead
    let headerRow = table.tHead.children[0];

    dataList.forEach( data => {
        let row = table.insertRow();
        Array.from(headerRow.children).forEach( column => {
            let cell = row.insertCell();
            let text = document.createTextNode(data[column.dataset.key]);
            cell.appendChild(text);
        });
    })
}

function fillOneRowTable(table, data) {
    //that's the row within the tbody
    let row = table.rows[0];

    Array.from(row.children).forEach( column => {
        let text = document.createTextNode(data[column.dataset.key]);
        column.appendChild(text);
    })
}