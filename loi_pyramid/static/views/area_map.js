import tables from '../utils/tables.js'
import accountCharactersData from '../models/account_characters.js'
import areaData from '../models/area.js'

const markup =
  `<table>
    </tbody> 
  </table>`

const renderMapTable = container => {
  // use of session here is problematic
  let areas = areaData.getData()
  let characters = accountCharactersData.getData(JSON.parse(sessionStorage.getItem('account')))

  return Promise.all([areas, characters]).then( ([areas, characters] = responses) => {
    tables.drawMap(document.querySelector(`#${container.id} table`), areas.areas, {endx: 6, endy: 11})
  })
  .catch( error => {
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
