import Template from '../utils/templates.js'
import characterTable from './character_table.js'
import accountTable from './account_table.js'

const markup =
  `<div id="accountInfo"></div>
  <div id="accountCharacters"></div>`

const templateMap = {
  accountInfo: accountTable,
  accountCharacters: characterTable
}

const accountCharacterPage = new Template.Page(
  'account_characters',
  markup,
  templateMap
)

export default accountCharacterPage
