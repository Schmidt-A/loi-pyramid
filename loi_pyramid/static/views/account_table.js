import tables from '../utils/tables.js'
import accountData from '../models/account.js'

const markup =
  `<table>
    <tbody>
      <tr>
        <th data-key="username"></th>
        <th data-key="role"></th>
        <th data-key="cdkey"></th>
        <th data-key="approved"></th>
        <th data-key="banned"></th>
        <th data-key="created"></th>
        <th data-key="updated"></th>
      </tr>
    </tbody>
  </table>`

const renderAccountTable = container => {
  // use of session here is problematic
  return accountData.getData(JSON.parse(sessionStorage.getItem('account')).username)
    .then(data => {
      tables.fillOneRowTable(document.querySelector(`#${container.id} table`), data)
    })
    .catch(error => {
      throw new Error(error.message)
    })
}

const accountTable = {
  markup: markup,
  listeners: [],
  dataset: accountData,
  renderData: renderAccountTable
}

export default accountTable
