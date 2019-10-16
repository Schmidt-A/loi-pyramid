import tables from '../utils/tables.js'
import accountCharactersData from '../models/account_characters.js'

const markup =
  `<table>
    <thead>
      <tr>
        <th data-key="name">Name</th>
        <th data-key="exp">Exp</th>
        <th data-key="area">Area</th>
        <th data-key="created">Created</th>
        <th data-key="updated">Updated</th>
      </tr>
    </thead>
    </tbody> 
  </table>`

const renderMapTable = container => {
  // use of session here is problematic
  return accountCharactersData.getData(JSON.parse(sessionStorage.getItem('account')))
    .then(data => {
      tables.fillTableFromHeader(document.querySelector(`#${container.id} table`), data.characters)
    })
    .catch(error => {
      throw new Error(error.message)
    })
}

const mapTable = {
  markup: markup,
  listeners: [],
  dataset: accountCharactersData,
  renderData: renderMapTable
}

export default mapTable
