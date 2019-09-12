function fillTableFromHeader(table, dataList) {
    //that's the row within the thead
    let headerRow = table.tHead.children[0]

    dataList.forEach( data => {
        let row = table.insertRow();
        Array.from(headerRow.children).forEach( column => {
            let cell = row.insertCell();
            let text = document.createTextNode(data[column.dataset.key]);
            cell.appendChild(text);
        });
    })
}