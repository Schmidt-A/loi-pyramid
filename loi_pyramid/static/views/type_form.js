import tables from '../utils/tables.js'
import templates from '../utils/templates.js'
import { searchData } from '../models/search.js'

const markup =
  `<input> </input>
  <table>
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
  </table>`

const accountListener = templates.listener(
  'input',
  'change',
  function (event) {
    event.preventDefault()
    console.log(event.srcElement.value)
    searchData.getData(event.srcElement.value)
      .then(data => {
        console.log(`fill table in ${event.srcElement.parentElement.id} from ${event.srcElement.value} with ${data.username}`)
        console.log(data)
        tables.fillOneRowTable(document.querySelector(`#${event.srcElement.parentElement.id} table`), data)
      })
      .catch(error => {
        console.error(error.message)
      })
  }
)

const logoutFunction = () => {
  if (sessionStorage.getItem('account')) {
    sessionStorage.clear()
    return fetch(`${BASE_URL}/logout`)
      .catch(error => {
        console.log(`logout: ${error.message}`)
      })
  } else {
    return Promise.resolve()
  }
}

export const searchAccountTable = {
  markup: markup,
  listeners: [accountListener],
  dataset: searchData,
  renderData: logoutFunction
}

const pageMarkup =
  '<div id="search"></div>'

const pageTemplateMap = {
  search: searchAccountTable
}

export const searchPage = templates.page(
  'search',
  pageMarkup,
  pageTemplateMap
)
