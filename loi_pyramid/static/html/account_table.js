import Template from '../js/template.js';
import Tables from '../js/tables.js';

let accountTableMarkup = 
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


const accountTable = new Template.Content(
  function () {},
  accountTableMarkup,
  function (data) {
    Tables.fillOneRowTable(document.querySelector(`#${this.container.id} table`), data);
  });
export default accountTable; 