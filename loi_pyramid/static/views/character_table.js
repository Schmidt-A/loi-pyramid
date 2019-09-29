import Templates from '../utils/templates.js'
import Tables from '../utils/tables.js'
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

const characterTable = new Templates.Template(
  accountCharactersData,
  markup,
  function () {
    return this.dataset.getData(JSON.parse(sessionStorage.getItem('account')))
      .then(data => {
        Tables.fillTableFromHeader(document.querySelector(`#${this.container.id} table`), data.characters)
      })
  },
  []
)

export default characterTable
