import templates from '../utils/templates.js'
import mapTable from './area_map.js'
import accountTable from './account_table.js'

const markup =
  `<div id="accountInfo"></div>
  <div id="mapTable"></div>`

const templateMap = {
  accountInfo: accountTable,
  mapTable: mapTable
}

const charactersMapPage = templates.page(
  'characters_map',
  markup,
  templateMap
)

export default charactersMapPage
