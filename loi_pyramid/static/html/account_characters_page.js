import Template from '../js/templates.js';
import characterTable from './character_table.js';
import accountTable from './account_table.js';
import Datasets from '../js/datasets.js';

let markup = 
  `<div id="accountInfo"></div>
  <div id="accountCharacters"></div>`;

let templateMap = {
  'accountInfo': accountTable,
  'accountCharacters': characterTable
};

const accountCharacterPage = new Template.Page(
  document.querySelector('#pageContainer'),
  'account_characters',
  markup,
  templateMap);

export default accountCharacterPage;