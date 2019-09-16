import Template from '../js/template.js';
import Tables from '../js/tables.js';

let characterTableMarkup = 
  `<table>
    <thead>
      <tr>
        <th data-key="name">Name</th>
        <th data-key="accountId">Owner</th>
        <th data-key="exp">Exp</th>
        <th data-key="area">Area</th>
        <th data-key="created">Created</th>
        <th data-key="updated">Updated</th>
      </tr>
    </thead>
    </tbody> 
  </table>`;

const characterTable = new Template.Content(
  'characterTable', 
  function () {},
  characterTableMarkup,
  function (dataList) {
    Tables.fillTableFromHeader(document.querySelector(`#characterTable table`), dataList);
  });

export default characterTable;