import Tables from '../tables.js';

let mockOneRow = {
    'mock': 1,
    'sample': 'asdf'
};

let mockMultiRows = [{
    'a': 1,
    'b': 2
},
{
    'a': 3,
    'b': 4
}];

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
    <tbody>
    </tbody>
</table>`;

let oneRowTable = document.querySelector('#oneRowTable');
let headerTable = document.querySelector('#headerTable');

beforeEach(() => {
    oneRowTable.innerHTML = 
    `<tbody>
        <tr>
            <th data-key="mock"></th>
            <th data-key="sample"></th>
        </tr>
    </tbody>`;

    headerTable.tBodies[0].innerHTML = '';
});


test('fillTableFromHeader()', () => {
    Tables.fillTableFromHeader(headerTable, mockMultiRows);

    expect(headerTable.tBodies[0].rows.length).toBe(2);

    let headerRow = headerTable.tHead.children[0];
    for (let i = 0; i < headerTable.tBodies[0].children.length; i++) {
        let row = headerTable.tBodies[0].rows[i];
        for (let j = 0; j < row.children.length; j++) {
            let cell = row.children[j];
            let headerCell = headerRow.children[j]
            expect(cell.textContent).toBe(mockMultiRows[i][headerCell.dataset.key].toString())
        }
    }
});

test('fillOneRowFromHeader()', () => {
    Tables.fillOneRowTable(oneRowTable, mockOneRow);

    expect(oneRowTable.rows.length).toBe(1);

    Array.from(oneRowTable.rows[0].children).forEach( cell => {
        expect(cell.textContent).toBe(mockOneRow[cell.dataset.key].toString())    
    });
});