import Template from '../js/template.js';
import characterTable from './character_table.js';
import accountTable from './account_table.js';

let accountCharacterMarkup = 
  `<div id="accountInfo"></div>
  <div id="accountCharacters"></div>`;

let accountTemplateMap = {
  'accountInfo': accountTable,
  'accountCharacters': characterTable
}
  
let loadData = function () {
  let account = JSON.parse(sessionStorage.getItem('account'));
  if (account && account.username) {
    fetch(`http://sundred.com:6543/accounts/${account.username}/characters`)
    .then(response => {
      parseResponse(response).then( characters => {
        this.characters = characters;
      })
    })
    .catch(error => {
      window.location = "login_stub.html"
    })
  } else {
    window.location = "login_stub.html"
  }
}

let renderData = function () {
  let account = JSON.parse(sessionStorage.getItem('account'));
  accountTable.afterRender(account);
  characterTable.afterRender(this.characters);
}

const loginPage = new Template.Page(
  'characters',
  loadData,
  accountCharacterMarkup,
  accountTemplateMap,
  renderData);

export default loginPage;