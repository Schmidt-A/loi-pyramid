import Templates from '../../../utils/templates.js';
import testCharacterTable from './character_table.js';
import testAccountTable from './account_table.js';
import testLoginForm from './login_form.js';

let wrapperMarkup = 
`<select id="pageOptions">
    <option value="">Pick a page</option>
    <option value="templateTester">Template Tester</option>
</select>

<div id="pageContainer"> </div>`;

let templatePageMarkup = 
`<div id="templateChoiceContainer"></div>`;

let templateChoiceMarkup = 
`<select id="templateOptions">
    <option value="">Pick a template</option>
    <option value="loginForm">Login Form</option>
    <option value="accountTable">Account Table</option>
    <option value="characterTable">Character Table</option>
</select>

<div id="contentContainer"></div>`;



let templateChoiceListener = new Templates.Listener(
'select',
'change',
function (event) {
  switch (event.target.value) {
  case 'loginForm':
  // try to use a spread operator for the template conversion
    let testLoginForm = new Templates.Content( 
      loginForm.dataset,
      loginForm.markup,
      loginForm.renderData,
      [new Templates.Listener(
        'form',
        'submit',
        function (event) {
          event.preventDefault();
            let formData = new FormData(event.srcElement);
            for (let input of formData.entries()) {
              console.log(`${input[0]}: ${input[1]}`)
            }
          },
        )],
      document.querySelector('#contentContainer'));
    testLoginForm.renderContent();
    break;
  case 'accountTable':
    let testAccountTable = new Templates.Content( 
      new Dataset(
        'account',
        function () {
          return Promise.resolve(accountFixture);
        }),
      accountTable.markup,
      accountTable.renderData,
      accountTable.listeners,
      document.querySelector('#contentContainer'));
    testAccountTable.renderContent();
    break;
  case 'characterTable':
    let testCharacterTable = new Templates.Content( 
      new Dataset(
        'accountCharacters',
        function () {
          return Promise.resolve(characterFixture);
        }),
      characterTable.markup,
      characterTable.renderData,
      characterTable.listeners,
      document.querySelector('#contentContainer'));
    testCharacterTable.renderContent();
    break;
  }
});

export let templateChoiceTemplate = new Templates.Template(
null,
templateChoiceMarkup,
function () {},
[templateChoiceListener]
);

let templatePageMap = {
'templateChoiceContainer': templateChoiceTemplate
};

export let templateChoicePage = new Templates.Page(
document.querySelector('#pageContainer'),
'template_test',
templatePageMarkup,
templatePageMap
);
