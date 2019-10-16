import templates from '../utils/templates.js'
import mapTable from './area_map.js'

const markup =
  `<div id="mapTable"></div>`

const templateMap = {
  mapTable: mapTable
}

const charactersMapPage = templates.page(
  'characters_map',
  markup,
  templateMap
)

export default charactersMapPage
