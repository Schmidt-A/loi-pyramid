import Templates from '../utils/templates.js';
import Tables from '../utils/tables.js';
import Datasets from '../utils/datasets.js';

let markup = 
  `<table>
    <tbody>
      <tr>
        <th data-key="username"></th>
        <th data-key="role"></th>
        <th data-key="approved"></th>
        <th data-key="banned"></th>
        <th data-key="created"></th>
        <th data-key="updated"></th>
      </tr>
    </tbody>
  </table>`;


const accountTable = new Templates.Template(
  Datasets.account,
  markup,
  function () {
    this.dataset.getData()
    .then( data => {
      Tables.fillOneRowTable(document.querySelector(`#${this.container.id} table`), data);
    })
  },
  []);
export default accountTable; 